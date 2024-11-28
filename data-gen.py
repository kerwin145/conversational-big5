import google.generativeai as genai
import csv
import time
import re


API_KEY = "" #api key to put
START, STOP = 600, 601

pattern = r"(Opengitness|Conscientiousness|Extraversion|Agreeableness|Neuroticism)\s+(.*?)(?=\s+(?:Openness|Conscientiousness|Extraversion|Agreeableness|Neuroticism)|$)"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def createPrompt(TEXT, cOPN, cCON, cEXT, cAGR, cNEU):
    # Convert 'y'/'n' to 'yes'/'no'
    cOPN = 'yes' if cOPN == 'y' else 'no'
    cCON = 'yes' if cCON == 'y' else 'no'
    cEXT = 'yes' if cEXT == 'y' else 'no'
    cAGR = 'yes' if cAGR == 'y' else 'no'
    cNEU = 'yes' if cNEU == 'y' else 'no'
    
    return f'''I will give you five questions, one for each category of the Big-5. I want you to answer these at about a paragraph length (3-5 sentences), attempting to address the question at hand. The important thing is that I will also give you an essay written by a person, and the Big-5 scores of that person in a yes/no format. I want you to use the essay and Big-5 scores as additional context/guidance to pretend to be that person in giving your responses to my first five questions. Also important: your output should include only the category of the question as a header followed by the answer, without any other formatting. For example: 

Openness 
<answer for openness>
Conscientiousness
<answer for conscientiousness> 
and so on…. 

Please keep this person's Big 5 scores in mind:
 Openness-{cOPN}, Conscientiousness-{cCON}, Extraversion-{cEXT}, Agreeableness-{cAGR}, Neuroticism-{cNEU} 

Here are the questions: 
Openness: Describe a time when you tried something completely new—whether it was a different activity, way of thinking, or environment. What motivated you to try it, and how did you feel about the experience afterward? 
Conscientiousness: Think of a goal you set for yourself that required sustained effort over time. How did you manage your time and resources to stay on track, and what strategies helped you stay committed, even when challenges came up? What did you find challenging or rewarding about the experience? 
Extraversion: Recall a memorable social experience that either energized you or left you feeling drained. What do you think made the interaction fulfilling or draining? How did it shape your understanding of your social preferences or needs? 
Agreeableness: Describe a situation where you found yourself in disagreement with someone. How did you handle the situation, and what were your priorities in resolving or understanding the conflict? 
Neuroticism: Think of a time when you felt particularly stressed or anxious. How did you respond initially, and what steps did you take to manage your emotions and approach the situation constructively? 

Lastly, here is the essay written by the person: 
{TEXT}
'''

# Function to handle rate limits and retries
def send_request_with_retry(model, prompt, idx):
    max_retries = 3
    retry_delay = 15  # seconds to wait before retrying

    for attempt in range(max_retries):
        try:
            # Make the API request
            response = model.generate_content(prompt)
            return response  # If successful, return the response
        except Exception as e:
            # Check for HTTP 429 or other exceptions
            if hasattr(e, 'code') and e.code == 429:  # HTTP 429: Too Many Requests
                print(f"Rate limit reached. Waiting {retry_delay} seconds before retrying (Attempt {attempt + 1})...")
                time.sleep(retry_delay)
            elif hasattr(e, 'code') and e.code == 403:  # HTTP 403: Daily limit or permission error
                print("Daily limit reached or permission denied. Stopping requests.")
                return "STOP"  # Signal to stop processing
            else:
                print(f"An unexpected error occurred: {e}. Retrying...")
                time.sleep(retry_delay)

    print("Max retries reached. Skipping this request.")
    return "STOP"

# Main processing loop
with open('essays.csv', mode='r') as file:
    reader = csv.DictReader(file)  # Automatically uses the first row as column names
    with open('train.csv', mode='a', newline='', encoding='utf-8') as outfile:
        fieldnames = ["idx", "textOPN", "textCON", "textEXT", "textAGR", "textNEU", "cOPN", "cCON", "cEXT", "cAGR", "cNEU"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        if outfile.tell() == 0: #writes the header only if file is empty
            writer.writeheader()

        for idx, row in enumerate(reader):
            if idx < START:
                continue
            if idx >= STOP:
                print(f"Reached limit. Stopped at row {idx-1}.")
                break
            print("Sending request")
            # Create the prompt
            prompt = createPrompt(row['TEXT'], row['cOPN'], row['cCON'], row['cEXT'], row['cAGR'], row['cNEU'])
            # Send the request with error checking
            response = send_request_with_retry(model, prompt, idx)

            # Check if the daily limit was reached
            if response == "STOP":
                print(f"Stopped at row {idx}.")
                break
            elif response:
                print(f"Request {idx} completed:")
                # print(response.text)
                text = response.text + "\n"
                matches = re.findall(pattern, text, re.DOTALL)
                sections = {header: paragraph.strip() for header, paragraph in matches}
                if len(sections) != 5 or not all(sections.get(header) for header in ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]):
                    print(f"Bad formatted output at idx {idx}. Saving it in a poor output text file")
                    with open("poor_output.txt", "a") as bad_output_file:
                            bad_output_file.write(f"Index {idx}:\n{text}\n\n")
                            break
                writer.writerow({'idx': idx, 
                                "textOPN" : sections["Openness"], 
                                "textCON" : sections["Conscientiousness"], 
                                "textEXT" : sections["Extraversion"], 
                                "textAGR" : sections["Agreeableness"],
                                "textNEU" : sections["Neuroticism"], 
                                "cOPN": row["cOPN"],
                                "cCON": row["cCON"], 
                                "cEXT": row["cEXT"], 
                                "cAGR": row["cAGR"], 
                                "cNEU": row["cNEU"] 
                            })
                print(f"Finished writing row {idx}")
outfile.close()