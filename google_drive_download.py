import gdown
import os
# change path to Users/markdaychman/Desktop

dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(f"{dir}/files")
url = 'https://drive.google.com/uc?id=1-O2a5aM0S763ZIIs5UujsPYdhxBY5U3S'

# gdown.download_folder(url)
gdown.download(url)
