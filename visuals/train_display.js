container = document.querySelector("#graphs")

const OPN = createBlock("Openness (OPN)", ["graphs/OPN_all.png", "graphs/OPN_top.png", "graphs/OPN_frozen.png"], ["All layers: 0.8414", "Top 4: 0.8381", "Fully Frozen: 0.5076"] ) 
const CON = createBlock("Conscientiousness (CON)", ["graphs/CON_all.png", "graphs/CON_top.png", "graphs/CON_frozen.png"], ["All layers: 0.9011", "Top 4: 0.9076", "Fully Frozen: 0.6126"] ) 
const EXT = createBlock("Extraversion (EXT)", ["graphs/EXT_all.png", "graphs/EXT_top.png", "graphs/EXT_frozen.png"], ["All layers: 0.8328", "Top 4: 0.8404", "Fully Frozen: 0.4775"] ) 
const AGR = createBlock("Agreeableness (AGR)", ["graphs/AGR_all.png", "graphs/AGR_top.png", "graphs/AGR_frozen.png"], ["All layers: 0.7646", "Top 4: 0.7881", "Fully Frozen: 0.3457"] ) 
const NEU = createBlock("Neuroticism (NEU)", ["graphs/NEU_all.png", "graphs/NEU_top.png", "graphs/NEU_frozen.png"], ["All layers: 0.7198", "Top 4: 0.714", "Fully Frozen: 0.4952"] ) 

container.appendChild(OPN)
container.appendChild(CON)
container.appendChild(EXT)
container.appendChild(AGR)
container.appendChild(NEU)

function createBlock(headerText, imagePaths, texts) {
    // Create a container div
    const container = document.createElement("div");
    container.className = "container"; // Use the container class

    // Create the header
    const header = document.createElement("h1");
    header.textContent = headerText;
    container.appendChild(header);

    // Create a wrapper for the images and texts
    const imageWrapper = document.createElement("div");
    imageWrapper.className = "image-wrapper"; // Use the image-wrapper class

    // Loop through the images and texts to create the groups
    for (let i = 0; i < 3; i++) {
        const group = document.createElement("div");
        group.className = "image-group"; // Use the image-group class

        const img = document.createElement("img");
        img.src = imagePaths[i];
        img.alt = texts[i];

        const label = document.createElement("p");
        label.textContent = texts[i];

        group.appendChild(img);
        group.appendChild(label);
        imageWrapper.appendChild(group);
    }

    // Append the wrapper to the container
    container.appendChild(imageWrapper);

    return container; // Return the container element
}
