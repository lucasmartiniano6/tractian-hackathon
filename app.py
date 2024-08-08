import streamlit as st
from PIL import Image

IMAGE_EXTENSIONS = [
    'jpeg',
    'jpg',
    'png',
    'svg'
]

SUBMIT = False

# Set the title of the app
st.title('Cadastro de itens novos')

with st.form('formCadastro'):
    # Input text box
    machineModelUserInput = st.text_input("Insira aqui o modelo da máquina:", disabled=SUBMIT)
    machineNameUserInput = st.text_input("Insira aqui o nome da máquina:", disabled=SUBMIT)
    machineManufacturerUserInput = st.text_input("Insira aqui o fabricante:", disabled=SUBMIT)

    st.text(body='Faça o upload de imagens de sua máquina:')

    image1 = st.file_uploader(label='Imagem 1', type=IMAGE_EXTENSIONS)
    image2 = st.file_uploader(label='Imagem 2', type=IMAGE_EXTENSIONS)
    image2 = st.file_uploader(label='Imagem 3', type=IMAGE_EXTENSIONS)

    if image1:
        st.image(image=Image.open((image1))) #display image 1

    st.divider()

    additionalUserInput = st.text_input('Gostaria de nos fornecer alguma informação adicional? Sinta-se livre!', 
                                        max_chars=500, 
                                        placeholder='Insira aqui as informações adicionais',
                                        disabled=SUBMIT)


    st.form_submit_button('Finalizar cadastro')