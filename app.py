import streamlit as st
from typing import List
import requests
import json
import base64
from webScrap import downloadItem
from pydantic import BaseModel
from detail import TechnicalDetail
import time

# Defining valid image extensions 
IMAGE_EXTENSIONS = [
    'jpeg',
    'jpg',
    'png',
    'svg'
]


MAPPING_KEYS = {
    'name': 'Name',
    'manufacturer': 'Manufacturer',
    'model': 'Model',
    'identification': 'Identification',
    'localization': 'Localization',
    'power': 'Power',
    'voltage': 'Voltage',
    'frequence': 'Frequence',
    'rotation': 'Rotation',
    'ip_rating': 'IP Rating',
    'operating_temperature': 'Operating Temperature',
    'current_state': 'Current State',
    'additional_info': 'Additional Info'
}

response = None

def callGPT(userInput: dict):
    '''
        This function takes dict containing the infos filled by the user and the uploaded images
        The values are uploaded to ChatGPT by an API and writes the response in the user screen
    '''
    response = requests.post(url='http://127.0.0.1:8000/', data=json.dumps(userInput))
    return response.json()



##############################################################################################
# START OF THE FRONT-END

st.image('tractian_no_background.png', width=500)

# Set the title of the app
st.title('Cadastro de itens novos')

#Set main form
with st.form('formCadastro', clear_on_submit=True):
    
    # Input text box
    machineModelUserInput = st.text_input("Insira aqui o modelo da máquina:")
    machineNameUserInput = st.text_input("Insira aqui o nome da máquina:")
    machineManufacturerUserInput = st.text_input("Insira aqui o fabricante:")

    st.divider() #Set a divider for styles

    # Image upload field
    st.text(body='Faça o upload de imagens de sua máquina:')
    image1 = st.file_uploader(label='Imagem 1', type=IMAGE_EXTENSIONS)
    image2 = st.file_uploader(label='Imagem 2', type=IMAGE_EXTENSIONS)
    image3 = st.file_uploader(label='Imagem 3', type=IMAGE_EXTENSIONS)


    # Set additional user input to help GPT // Not required
    additionalUserInput = st.text_input('Gostaria de nos fornecer alguma informação adicional? Sinta-se livre!', 
                                        max_chars=500, 
                                        placeholder='Insira aqui as informações adicionais',
                                        )


    submitted = st.form_submit_button('Submeter para análise')
    
    if submitted: #If submitted then callGPT
        encoded = [
            base64.b64encode(image1.getvalue()).decode('utf-8'),
            base64.b64encode(image2.getvalue()).decode('utf-8'),
            base64.b64encode(image3.getvalue()).decode('utf-8')
        ]

        inputs = {
            'machineName': machineNameUserInput, 
            'machineModel': machineModelUserInput, 
            'machineManufacturer': machineManufacturerUserInput, 
            'images': encoded,
            'additionalInfo': additionalUserInput
        }
        
        response = callGPT(userInput=inputs)
        response = json.loads(response)
        
if response:
    st.divider()
    with st.container(border=True):
        st.header('**Ficha técnica do maquinário**')
        
        try: #tentar pegar a imagem do google
            imgFetch = downloadItem(response['name'])
            if imgFetch:
                st.image(imgFetch)

        except: #nao rolou de pegar a imagem no google
            pass

        try:
            details = TechnicalDetail.parse_obj(response)
            if details:
                detailsDict = details.dict()
                
                for key, value in detailsDict.items():
                    st.write(f'**{MAPPING_KEYS[key]}**: {value}')
        except:
            st.write('Houve um erro. Tente novamente')

@st.dialog('Item cadastrado com sucesso!')
def finalDialog():
    pass

if st.button('Finalizar cadastro'):
    finalDialog()
