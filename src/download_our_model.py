import requests
from zipfile import ZipFile

ZIP_PATH='our_model.zip'

def download():
    URL = "https://drexel-cs583-final.s3.us-east-2.amazonaws.com/our_model.zip"

    session = requests.Session()
    response = session.get(URL, stream = True)

    save_response_content(response, ZIP_PATH)

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)



print('Dowloading Sony Model (82Mb)')

download()
ZipFile(ZIP_PATH).extractall(path='.')
