def readMeta(self):
    opfpath= (os.path.join(self.outputdirSplashOnlyname,"META-INF/container.xml"))
    imagePath = ""
    textPath = ""
    contents = Path(opfpath).read_text()
    contents = re.sub(' xmlns="[^"]+"', '', contents, count=1)
    contents = contents.encode('utf-8')
    root = etree.fromstring(contents)
    for item in root.findall(".//manifest/"):
        href = item.attrib["href"]
        if imagePath == "" and re.search('image', href, re.IGNORECASE):
            imagePath = os.path.dirname(href)

        if textPath == "" and re.search('text', href, re.IGNORECASE):
            textPath = os.path.dirname(href)

        if imagePath != "" and textPath != "":
            break

    return imagePath, textPath
