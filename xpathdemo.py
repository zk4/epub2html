import zipfile
with zipfile.ZipFile("./a.epub", 'r') as zip_ref:
    zip_ref.extractall("./demo")
