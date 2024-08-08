from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI
from detail import TechnicalDetail


# Defining UserInput class for typing
class UserInput(BaseModel):
    machineName: str
    machineModel: str
    machineManufacturer: str
    images: List[str]

def analyze_images(query: str, images: List[str]):
    """Query GPT-4 Vision to analyze the given images with the json as context."""
    assert len(images) == 3

    load_dotenv()
    client = OpenAI()
    response = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {
        "role": "system",
        "content": "You are an expert in the industrial machine area and are able to recognize and extract technical details about any machine just by looking at it's images and knowing it's name, model and manufacturer. If you are unsure about a certain technical detail, be clear about it. Do not make up factual information and search the images and the web whenever possible."
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": query
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{images[0]}"
            },
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{images[1]}"
            },
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{images[2]}"
            },
            }
        ],
        }
    ],
    response_format=TechnicalDetail
    )
    return response.choices[0].message.content


app = FastAPI()

@app.post('/') #Post GPT response
def inference(userInput: UserInput):

    query = f"""
    You are presented with images from a machine that has the model {userInput.machineModel},
    manufacturer {userInput.machineManufacturer} and name {userInput.machineName}. Now analyze the image
    and present detailed technical information about this particular machine. Return as a JSON file.
    """

    return analyze_images(query=query, images=userInput.images)