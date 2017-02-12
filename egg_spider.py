from lxml import etree
import requests
from io import StringIO, BytesIO



header_info = {'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}


url = "http://www.42.fr/les-demarches-administratives/"

r = requests.get(url, headers=header_info, timeout=5)


parser = etree.HTMLParser()
tree = etree.parse(StringIO(r.text), parser)
root = tree.getroot()

found_metas = {}

title = root.xpath("//head/title")
for met in title:
    found_metas['title'] = met.text

h1 = root.xpath("//h1[1]")
for h in h1:
    found_metas['h1'] = h.text


# found_metas['title']


