import requests
import os
import sys
from zipfile import ZipFile

OUTDIR='./dataset'

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 327680
    downloaded = 0
    total = 26926678016.00 * 1.0828 / 100.00
    sys.stdout.write("\r0.00% done")
    sys.stdout.flush()

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                downloaded+=CHUNK_SIZE
                if downloaded % (CHUNK_SIZE*1000) == 0:
                    sys.stdout.write('\r%0.2f%% done' % (downloaded/(total)))

# Ensure directory exists
if not os.path.exists(OUTDIR):
  os.mkdir(OUTDIR)

filepath = OUTDIR+'/Sony.zip'
# Too much data, download the smaller dataset for now
if not os.path.exists(filepath):
  print('Dowloading Sony subset... (25GB)')
  download_file_from_google_drive('10kpAcvldtcb9G2ze5hTcF1odzu4V_Zvh', filepath)

fileout = OUTDIR+'/Sony'
# Always unzip to reset directory
if not os.path.exists(fileout):
  print('\nUnzipping...')
  ZipFile(filepath).extractall(path=fileout)

print("Data ready in %s" % (fileout))
