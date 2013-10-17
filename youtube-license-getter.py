import urllib
import sys
import os

from lxml import etree


def get_licence(url):
    htmlstr = urllib.urlopen("{video}".format(video=url)).read()
    html = etree.HTML(htmlstr)

    h4s = [h4 for h4 in html.findall('.//h4') if h4.attrib.get('class') == 'title']
    license = "Not Found"
    for i, h4 in enumerate(h4s):
        if "license" in h4.text.strip().lower():
            license = "".join([t for t in h4.getnext().itertext()]).strip()

    return license


def getvideolinks(xml):
    links = []

    for video in xml.findall('.//link'):
        url = video.attrib.get('url')
        if ("youtube" in url) or (r'youtu.be' in url):
            links.append(url)
        else:
            print ",".join([url, "not youtube"])

    return links



urls = []

if __name__ == "__main__":

    folder = os.path.abspath("/home/ewald/Books/gr4-6-workbooks")

    for dirpath, dirnames, filenames in os.walk(folder):
        for f in filenames:
            if f.endswith('index.cnxmlplus'):
                xml = etree.parse(os.path.join(dirpath,f))
                links = getvideolinks(xml)
                for link in links:
                    if link not in urls:
                        urls.append(link)


    for url in urls:
        print ",".join([url, get_licence(url)])
