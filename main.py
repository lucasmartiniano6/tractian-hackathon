from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI
from detail import TechnicalDetail
import base64, json

class UserInput(BaseModel):
    """
    Defining UserInput class for typing
    """
    machineName: str
    machineModel: str
    machineManufacturer: str
    images: List[str]

def encode_image(image_path: str):
  """
  Helper function to encode the image as Base64
  """
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

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
        "content": """
        You are an expert mechanical engineer working in the industrial equipment and machinery area with decades of work experience. You are able to
        analyze, recognize and extract technical details about any machine just by looking at it and knowing it's name, model and manufacturer.
        Your were hired by TRACTIAN, an innovative company specializing in sensors and predictive maintenance for machinery. Your role is 
        to ensure that the information about the machines is highly detailed, accurate, and useful for the maintenance team and predictive analysis.
        If you are unsure about a certain technical detail, be clear about it and express your concerns. Do not make up factual information. 
        Search in the images provided and query the web whenever necessary. Given the importance of efficiency and reliability for our operations, 
        it is crucial to scrutinize every aspect of the machine, including its current condition, quality, and any potential areas of concern that 
        may affect performance.
        """
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
    # This is the query used by the User application
    query = f"""
    You are presented with 3 images from a machine that has the model "{userInput.machineModel}", manufacturer "{userInput.machineManufacturer}"
    and name "{userInput.machineName}". Now analyze the image and present detailed technical information about this particular machine.
    Usually, you will receive 2 images of the machine itself as seen from the outside and 1 final image with the derating details of it.
    This final particular image with the details is the most important one, be very aware and cautious with it. You must pay attention to 
    all details of this image, as it tells you the most about the machine you are working with. You have more trust in the derating details 
    image than in the other ones. 

    Task:
    Create a highly detailed and informative technical datasheet for the machine using the provided information.

    Steps:
    Receive and analyze the images and data provided
    Thoroughly review the provided images of the machine and its data
    Pay close attention to all visible details, including the condition of the machine, signs of wear or damage, quality of components, and any other elements that might impact the machine's performance and maintenance needs.
    Identify any components that appear to be outdated, worn, or in need of repair or replacement.
    Develop the Technical Datasheet
    
    General Description:
    Provide a comprehensive overview of the machine, including its primary function, design features, and operational capabilities.
    Discuss the machine's role within the broader industrial process, highlighting its importance to operational efficiency.
    Detailed Technical Specifications:
    Include exhaustive technical details such as power output, voltage, frequency, protection class, efficiency, operational limits, and mechanical characteristics.
    Specify the condition of key components, including any observable signs of wear or degradation.
    Detail any environmental factors the machine may be exposed to and how these might affect performance (e.g., dust, humidity, temperature variations).
    Highlight any areas that may require closer inspection, maintenance, or immediate attention.
    Additional Relevant Information:
    Include any extra details that will assist in understanding the machine's maintenance needs, operational efficiency, and potential risks.
    Provide recommendations for maintenance schedules, spare parts to keep on hand, and any upgrades that may enhance the machine's performance or longevity.
    Discuss the compatibility of the machine with TRACTIAN's predictive maintenance sensors, outlining how these could be used to monitor critical aspects of the machine's operation.

    Verify Accuracy:
    Ensure that all the information provided is precise and corresponds directly to the images and data available.
    Double-check the correctness of technical details, ensuring they match industry standards and the specifications provided by the machine's manufacturer.
    Validate any observations regarding the machine's condition with a focus on accuracy and practical implications for maintenance.

    Review and Adjust:
    Carefully review the datasheet for clarity, completeness, and usability.
    Make necessary adjustments to improve readability, ensuring that the document is accessible to the maintenance team and other stakeholders.
    Enhance the datasheet by adding any relevant insights or considerations that could improve the machine's operational efficiency or predictive maintenance processes.

    Context:
    TRACTIAN uses sensors to monitor and predict maintenance needs for industrial machines. The technical datasheet should provide extensive, detailed information that supports predictive analysis and effective machine maintenance, ultimately aiming to optimize operational efficiency and reduce downtime.
    
    Constraints:
    The datasheet must be based exclusively on the provided images and data.
    Ensure that the information is accurate, detailed, and relevant for TRACTIAN's maintenance and predictive analysis teams.
    Avoid including assumptions or unverified data. Stick to observable facts and verified information only.

    Objectives:
    Create a datasheet that delivers a clear, detailed, and comprehensive overview of the machine.
    Provide information that aids the maintenance team in understanding, monitoring, and maintaining the machine.
    Ensure the datasheet meets TRACTIAN's high standards for technical documentation, focusing on detail, accuracy, and practical usability.

    Output:
    A well-structured, detailed technical datasheet for the machine that includes all of its technical details including but not limited to power output, voltage, frequency, protection class, current condition, potential risks, and other critical technical information.
    Also, additional relevant information: Insights and recommendations that support effective maintenance, predictive analysis, and operational efficiency.
    """

    return analyze_images(query=query, images=userInput.images)

if __name__ == "__main__":
    # Here we run the gpt4o API in the folders and write out the outputs. We use it to test our prompts in various scenarios
    # This part was only used for local testing and it's not necessary when running the full application
    pastas = [1, 2, 3, 4, 5, 10]
    for pasta in pastas:
        with open(f"{pasta}/asset_info.json") as f:
            assets = json.load(f)
        machineModel = assets['model']
        machineName = assets['name']
        machineManufacturer = assets['manufacturer']

        paths = [f"{pasta}/img1.jpg", f"{pasta}/img2.jpg", f"{pasta}/img3.jpg"]
        images = []
        for p in paths:
            images.append(encode_image(p))

        query = f"""
        You are presented with 3 images from a machine that has the model "{machineModel}", manufacturer "{machineManufacturer}"
        and name "{machineName}". Now analyze the image and present detailed technical information about this particular machine.
        Usually, you will receive 2 images of the machine itself as seen from the outside and 1 final image with the derating details of it.
        This final particular image with the details is the most important one, be very aware and cautious with it. You must pay attention to 
        all details of this image, as it tells you the most about the machine you are working with. You have more trust in the derating details 
        image than in the other ones. 

        Task:
        Create a highly detailed and informative technical datasheet for the machine using the provided information.

        Steps:
        Receive and analyze the images and data provided
        Thoroughly review the provided images of the machine and its data
        Pay close attention to all visible details, including the condition of the machine, signs of wear or damage, quality of components, and any other elements that might impact the machine's performance and maintenance needs.
        Identify any components that appear to be outdated, worn, or in need of repair or replacement.
        Develop the Technical Datasheet
        
        General Description:
        Provide a comprehensive overview of the machine, including its primary function, design features, and operational capabilities.
        Discuss the machine's role within the broader industrial process, highlighting its importance to operational efficiency.
        Detailed Technical Specifications:
        Include exhaustive technical details such as power output, voltage, frequency, protection class, efficiency, operational limits, and mechanical characteristics.
        Specify the condition of key components, including any observable signs of wear or degradation.
        Detail any environmental factors the machine may be exposed to and how these might affect performance (e.g., dust, humidity, temperature variations).
        Highlight any areas that may require closer inspection, maintenance, or immediate attention.
        Additional Relevant Information:
        Include any extra details that will assist in understanding the machine's maintenance needs, operational efficiency, and potential risks.
        Provide recommendations for maintenance schedules, spare parts to keep on hand, and any upgrades that may enhance the machine's performance or longevity.
        Discuss the compatibility of the machine with TRACTIAN's predictive maintenance sensors, outlining how these could be used to monitor critical aspects of the machine's operation.

        Verify Accuracy:
        Ensure that all the information provided is precise and corresponds directly to the images and data available.
        Double-check the correctness of technical details, ensuring they match industry standards and the specifications provided by the machine's manufacturer.
        Validate any observations regarding the machine's condition with a focus on accuracy and practical implications for maintenance.

        Review and Adjust:
        Carefully review the datasheet for clarity, completeness, and usability.
        Make necessary adjustments to improve readability, ensuring that the document is accessible to the maintenance team and other stakeholders.
        Enhance the datasheet by adding any relevant insights or considerations that could improve the machine's operational efficiency or predictive maintenance processes.

        Context:
        TRACTIAN uses sensors to monitor and predict maintenance needs for industrial machines. The technical datasheet should provide extensive, detailed information that supports predictive analysis and effective machine maintenance, ultimately aiming to optimize operational efficiency and reduce downtime.
        
        Constraints:
        The datasheet must be based exclusively on the provided images and data.
        Ensure that the information is accurate, detailed, and relevant for TRACTIAN's maintenance and predictive analysis teams.
        Avoid including assumptions or unverified data. Stick to observable facts and verified information only.

        Objectives:
        Create a datasheet that delivers a clear, detailed, and comprehensive overview of the machine.
        Provide information that aids the maintenance team in understanding, monitoring, and maintaining the machine.
        Ensure the datasheet meets TRACTIAN's high standards for technical documentation, focusing on detail, accuracy, and practical usability.

        Output:
        A well-structured, detailed technical datasheet for the machine that includes all of its technical details including but not limited to power output, voltage, frequency, protection class, current condition, potential risks, and other critical technical information.
        Also, additional relevant information: Insights and recommendations that support effective maintenance, predictive analysis, and operational efficiency.
        """
        res = analyze_images(query, images)
        with open(f"{pasta}/out.txt", "w") as f:
            f.write(res)
        print(f"Done with {pasta}")
        #print(res)