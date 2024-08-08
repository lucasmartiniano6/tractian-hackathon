# Hackathon TRACTIAN 

Usage
-----
To install run:
```install
./pip install -r requirements.txt
```
That's it! Now run this command to start the server:
```run
uvicorn main:app --reload
```
Finally, open up a new terminal to run the web app:
```run
streamlit run app.py
```

Using ChatGPT4 to identify the images
-----
We are using gpt-4o to analyze the image and parse the results into a pydantic JSON object. This is done using the **structured outputs** feature of the OpenAI API, which automatically parses and forces the results to the corresponding JSON file. We use 2 types of prompts, one for the system and other for the user. The first one is simpler, we tell the agent to pretend he's an experienced mechanical engineer hired by TRACTIAN - an innovative company specializing in sensors and predictive maintenance for machinery-, then we ask him to write a technical report about a particular machine. The latter prompt is more complex, we emphasize the fact that the Agent will receive three images but the most important one is the one with the machine plate, which contains the derating details of the particular machine. Furthermore, we describe step-by-step what the Agent should do to analyse this plate and look at the relevant details. We also emphasize a lot that whenever he's unsure about something, he should **NOT** make up factual information, and to express his concerns saying that he's not sure about some particular information. He should only use the images and data provided to draft the technical report.

FastAPI and Streamlit
-----


Results
-----

Nice TODO:
-----

Refs:
-----
* 
    