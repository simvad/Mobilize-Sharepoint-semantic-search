import requests
from bs4 import BeautifulSoup
import os
from PyPDF2 import PdfReader

if not os.path.exists('storage'):
    os.makedirs('storage')

url = 'https://mobilize-nordic.com/det-faglige-univers/?c=artikler&s=&v=all#more'
response = requests.get(url, timeout=5)
content = BeautifulSoup(response.content, "html.parser")

cards = content.find_all("div", {"class": ["card", "imagecard"]})

#Download all articles

with open("storage/artikler.txt", "a", encoding='utf-8') as f:
    for card in cards:
        card_link = card.find("a")
        if card_link and "podcast" not in card_link["href"] and "nyhedsbrev" not in card_link["href"]:
            link = "https://mobilize-nordic.com" + card_link["href"]
            response = requests.get(link, timeout=5)
            content = BeautifulSoup(response.content, "html.parser")
            try:
                download_div = content.find("div", {"class": "download"})
                if download_div:
                    download_link = "https://mobilize-nordic.com" + download_div.find("a")["href"]
                    response = requests.get(download_link, timeout=5)
                    filename = download_link.split("/")[-1]

                    if filename.endswith(".pdf"):
                        pdf_file = open("temp.pdf", 'wb')
                        pdf_file.write(response.content)
                        pdf_file.close()

                        pdf_file = open("temp.pdf", 'rb')
                        pdf_reader = PdfReader(pdf_file)
                        for page in pdf_reader.pages:
                            f.write(page.extract_text())

            except Exception as e:
                print(f"Error processing link {link}: {e}")

#Donwload all books
url = 'https://mobilize-nordic.com/det-faglige-univers/?c=boger#filter'
response = requests.get(url, timeout=5)
content = BeautifulSoup(response.content, "html.parser")

cards = content.find_all("div", {"class": ["card", "imagecard"]})

with open("storage/bøger.txt", "a", encoding="utf-8") as f:
    for card in cards:
        card_link = card.find("a")
        if card_link and "podcast" not in card_link["href"] and "nyhedsbrev" not in card_link["href"]:
            link = "https://mobilize-nordic.com" + card_link["href"]
            response = requests.get(link, timeout=5)
            content = BeautifulSoup(response.content, "html.parser")
            try:
                download_div = content.find("div", {"class": "download"})
                if download_div:
                    download_link = "https://mobilize-nordic.com" + download_div.find("a")["href"]
                    response = requests.get(download_link, timeout=5)
                    filename = download_link.split("/")[-1]

                    if filename.endswith(".pdf"):
                        pdf_file = open("temp.pdf", 'wb')
                        pdf_file.write(response.content)
                        pdf_file.close()

                        pdf_file = open("temp.pdf", 'rb')
                        pdf_reader = PdfReader(pdf_file)
                        for page in pdf_reader.pages:
                            page_text = page.extract_text()
                            f.write(page_text)

            except Exception as e:
                print(f"Error processing link {link}: {e}")

#append boger.txt to artikler.txt in a new file all.txt

with open("storage/artikler.txt", "r", encoding='utf-8') as f:
    artikler = f.read()
with open("storage/bøger.txt", "r", encoding='utf-8') as f:
    boger = f.read()
with open("storage/all.txt", "w", encoding='utf-8') as f:
    f.write(artikler)
    f.write(boger)
