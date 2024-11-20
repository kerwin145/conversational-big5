import asyncio
import aiohttp
import csv
from aiolimiter import AsyncLimiter  # For rate-limiting
from datetime import datetime

# Configure API Key
API_KEY = "My-key"
BASE_URL = "https://api.example.com/generate_content"  # Replace with the actual endpoint
MAX_WORKERS = 10
RATE_LIMIT = AsyncLimiter(max_rate=15, time_period=60)  # 15 requests per minute

# Function to create prompt
def createPrompt(TEXT, cOPN, cCON, cEXT, cAGR, cNEU):
    return f"Process this text: {TEXT} with traits OPN={cOPN}, CON={cCON}, EXT={cEXT}, AGR={cAGR}, NEU={cNEU}"

# Async function to make API request
async def send_request(session, row, idx, pause_event):
    async with RATE_LIMIT:  # Enforce rate limiting
        try:
            # Wait if the pause_event is set
            await pause_event.wait()

            # Create the prompt
            prompt = createPrompt(row['TEXT'], row['cOPN'], row['cCON'], row['cEXT'], row['cAGR'], row['cNEU'])

            # Send the request
            async with session.post(BASE_URL, json={"prompt": prompt, "api_key": API_KEY}) as response:
                if response.status == 429:  # Rate limit hit
                    print(f"Rate limit reached for request {idx}. Pausing...")
                    pause_event.clear()  # Pause workers
                    await asyncio.sleep(15)  # Wait for rate reset
                    pause_event.set()  # Resume workers
                elif response.status == 403:  # Daily limit or permission denied
                    print("Daily limit reached. Stopping...")
                    return "STOP"
                elif response.status >= 400:
                    print(f"Error for request {idx}: {response.status}")
                    return None

                # Parse the response
                result = await response.json()
                print(f"Request {idx} completed.")
                return {"index": idx, "response": result["text"]}  # Adjust based on actual API response
        except asyncio.TimeoutError:
            print(f"Timeout for request {idx}. Pausing...")
            pause_event.clear()
            await asyncio.sleep(15)  # Pause briefly on timeout
            pause_event.set()
            return None

# Async function to handle worker tasks
async def worker(queue, session, pause_event, writer):
    while True:
        task = await queue.get()
        if task is None:
            break  # Exit when all tasks are completed

        row, idx = task
        result = await send_request(session, row, idx, pause_event)
        if result == "STOP":
            break
        elif result:
            # Save response to CSV
            writer.writerow({"Index": result["index"], "Response": result["response"]})

        queue.task_done()

# Main function
async def main():
    pause_event = asyncio.Event()
    pause_event.set()  # Allow workers to start

    # Open CSV files for reading and writing
    input_file = 'essays.csv'
    output_file = 'responses.csv'

    with open(input_file, mode='r') as infile, open(output_file, mode='w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ["Index", "Response"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        # Create an asyncio queue and load tasks
        queue = asyncio.Queue()
        for idx, row in enumerate(reader):
            await queue.put((row, idx))

        # Create a session and worker pool
        async with aiohttp.ClientSession() as session:
            tasks = [
                asyncio.create_task(worker(queue, session, pause_event, writer))
                for _ in range(MAX_WORKERS)
            ]

            # Wait for the queue to be processed
            await queue.join()

            # Stop workers
            for _ in range(MAX_WORKERS):
                await queue.put(None)

            await asyncio.gather(*tasks)

# Run the async main function
asyncio.run(main())
