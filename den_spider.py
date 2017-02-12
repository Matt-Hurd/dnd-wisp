

from lxml import etree
import requests
from io import StringIO, BytesIO
from urllib.parse import urlparse, parse_qs
import psycopg2






r = requests.get('https://www.squarespace.com/')

# print (r.text)


parser = etree.HTMLParser()


tree = etree.parse(StringIO(r.text), parser)

root = tree.getroot()

links = tree.xpath("//a/@href")
head = root.xpath("//head")
metas = root.xpath("//head/meta") 


# print (root.tag)


# a = dir(root)

# print (a)

# print (root)
print (links)
# print (head)
# print (metas)

output = [{}]

# print ()
# print (dir(links[0]))

# parsed_url = urlparse(links[0])

# print ()
# print ("link: {a}".format(a=links[0]))
# print ("parsed_url: {b}".format(b=parsed_url))
# # print (dir(parsed_url))
# print ()

for i, link in enumerate(links):
    parsed = urlparse(link)    
    if parsed.netloc:
        print("{i}: netloc: {v}".format(i=i, v=parsed.netloc))
        print (parsed)
        print ("url: {u}".format(u=link))
        print ()


# for index, link in enumerate(links):
#     print ("links: {a}".format(a=link))
#     print ("\tparsed: {b}".format(b=urlparse(link)))




# for index, elm in enumerate(metas):
    # print ("{index}: tag: {a}, text: {b}".format(index=index, a=elm.tag, b=elm.text))
#     for i, keys in enumerate(elm.keys()):
#         print ("\t{i}: {c} = '{d}'".format(i=i, c=keys, d=elm.values()[i]))
    
    

# result = etree.tostring(tree.getroot(), pretty_print=True, method="html")
# 
# print ("dfaofhaodhfo")

# print (result)













