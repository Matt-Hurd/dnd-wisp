

from lxml import etree
import requests
from io import StringIO, BytesIO

r = requests.get('https://www.squarespace.com/')

# print (r.text)


parser = etree.HTMLParser()


tree = etree.parse(StringIO(r.text), parser)

root = tree.getroot()

links = tree.xpath("//a")
head = root.xpath("//head")
metas = root.xpath("//head/meta") 


print (root.tag)

# a = dir(root)

# print (a)

# print (root)
print (links)
print (head)
print (metas)

print (dir(metas[0]))



for index, elm in enumerate(metas):
    print ("{index}: tag: {a}, text: {b}".format(index=index, a=elm.tag, b=elm.text))
    for i, keys in enumerate(elm.keys()):
        print ("\t{i}: {c} = '{d}'".format(i=i, c=keys, d=elm.values()[i]))
    
    

# result = etree.tostring(tree.getroot(), pretty_print=True, method="html")
# 
# print ("dfaofhaodhfo")

# print (result)













