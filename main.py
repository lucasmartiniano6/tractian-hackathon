from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openai import OpenAI
import base64

class TechnicalDetail(BaseModel):
    name: str = Field(..., description="Name of the machine")
    manufacturer: str = Field(..., description="Manufacturer of the machine")
    model: str = Field(..., description="Model of the machine")

    identification: str
    localization: str
    power: str
    voltage: str
    frequence: str
    rotation: str
    ip_rating: str = Field(..., description="IP Rating of the machine")
    operating_temperature : str = Field(..., description="Operating Ambient Temperature")

    current_state: str = Field(..., description="Description of the currente state of the machine based on the given images")
    additional_info: str = Field(..., description="Any additional information about the machine that might be useful.")

def encode_image(image_path):
  """Helper function to encode the image as Base64"""
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_images(query: str, paths: List[str]):
    """Query GPT-4 Vision to analyze the given images with the json as context."""
    images = [] 
    for img_path in paths:
       images.append(encode_image(img_path))
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
    #max_tokens=1000,
    response_format=TechnicalDetail
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    name = "10009204 - MOTOR ROLOS FIXO (LADO B) 40CV"
    manufacturer = "WEG"
    model = "electricMotor-threePhase"
    query = f"""
    You are presented with images from a machine that has the model {model},
    manufacturer {manufacturer} and name {name}. Now analyze the image
    and present detailed technical information about this particular machine. Return as a JSON file.
    """

    res = analyze_images(query, ["1/img1.jpg", "1/img2.jpg", "1/img3.jpg"])
    print(res)