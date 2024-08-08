import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

def searchFirstImage(query: str):
    # Build URL given a query
    query = query.replace(' ', '+')
    url = f"https://www.google.com/search?q={query}&tbm=isch"

    # Define o User-Agent para evitar bloqueio
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    
    # Faz a requisição para o Google Imagens
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Procura a primeira imagem nos resultados
    img_tags = soup.find_all("img")
    if img_tags:
        img_url = img_tags[1].get("src")  # O primeiro `img` geralmente é o logo do Google, então pegamos o segundo
        return img_url
    else:
        return None

def downloadImage(imgUrl):
    # Faz o download da imagem
    response = requests.get(imgUrl)
    return Image.open(BytesIO(response.content))

def downloadItem(item):
    img_url = searchFirstImage(item)
    if img_url:
        return downloadImage(img_url)
