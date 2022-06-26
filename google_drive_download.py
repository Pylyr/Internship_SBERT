import gdown
import os

dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(f"{dir}/files")
# url = 'https://drive.google.com/uc?id=1-O2a5aM0S763ZIIs5UujsPYdhxBY5U3S'
url = 'https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/'

# gdown.download_folder(url)
gdown.download(url)
