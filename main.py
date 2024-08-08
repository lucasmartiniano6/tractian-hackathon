from typing import List
from dotenv import load_dotenv
from openai import OpenAI
import base64
from fastapi import FastAPI

# Helper function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def query_gpt(query: str, paths: List[str]):
    # images = [] 
    # for img_path in paths:
    #    images.append(encode_image(img_path))
    assert len(paths) == 3

    load_dotenv()
    client = OpenAI()
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
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
    max_tokens=300,
    )
    return response.choices[0]

app = FastAPI()

@app.post('/')
def inference():
    return query_gpt("what are those digits?", ["digito.png", "digito5.jpeg", "digito.png"])