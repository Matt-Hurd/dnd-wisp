

from lxml import etree
import requests
from io import StringIO, BytesIO
from urllib.parse import urlparse, parse_qs
import psycopg2




# conn = psycopg2.connect("dbname='dnd_database' user='postgres' host='138.197.194.84' password='a54fd22438e9e5892c0921405e339e19' port='26606'")


# cur = conn.cursor()

# lim = 10
# # reset_scraped = True;
# reset_scraped = False;

# distinct = "select distinct on (domain) * from urls where scraped = '0' limit {lim};".format(lim=lim)
# update_scraped = "update urls set scraped='1' where {temp};"
# q_reset_scraped = "update urls set scraped='0';"



# cur.execute(distinct)

# rows = cur.fetchall()



# ids = ""
# if (rows):
#     for i, row in enumerate(rows):
#         if (i == 0):
#             ids = "id={idd}".format(idd=row[0])
#         else:
#             ids += "or id={idd}".format(idd=row[0])

            
#     # print (update_scraped.format(temp=ids))
#     cur.execute(update_scraped.format(temp=ids))

#     conn.commit()


#     # print ("len: {l}".format(l=len(rows)))
#     # print (rows)

# if (reset_scraped):
#     cur.execute(q_reset_scraped)
#     conn.commit()


# # t.string   "url"
# # t.string   "domain"
# # t.string   "path"
# # t.boolean  "scraped"
# # t.integer  "counter"
# # t.datetime "created_at", null: false
# # t.datetime "updated_at", null: false
# # t.index ["url"], name: "index_urls_on_url", using: :btree




































# r = requests.get('https://gorails.com/')
r = requests.get('https://css-tricks.com/')




parser = etree.HTMLParser()


tree = etree.parse(StringIO(r.text), parser)

root = tree.getroot()

links = tree.xpath("//a/@href")
# head = root.xpath("//head")
# metas = root.xpath("//head/meta") 

link_output = []
#     url_val=rows[0][1],
#     domain_val=rows[0][2],
#     path_val=rows[0][3],
#     scraped_val=rows[0][4],


url_insert = ""
url_columns = "(url, domain, path, scraped, created_at, updated_at)"
found_urls = set()
for i, link in enumerate(links):
    parsed = urlparse(link)    
    if parsed.netloc:
        url = link.split('?')[0].split('#')[0]
        if not (url in found_urls):
            found_urls.add(url)        
            url_insert += "('{url_val}', '{domain_val}', '{path_val}', {scraped_val}, now(), now())".format(
                    url_val=url,
                    domain_val=parsed.netloc,
                    path_val=parsed.path,
                    scraped_val=False,                
                )



# for i, link in link_output:
#     print ()
#     print (link)
#     insert_link





print ()
print (url_columns)
print (url_insert)



# insert = "INSERT INTO urls \
# (url, domain, path, scraped, created_at, updated_at) \
# VALUES ('{url_val}', '{domain_val}', '{path_val}', {scraped_val}, now(), now())\
# ON CONFLICT (url) DO NOTHING;\
# ".format(
#     url_val=rows[0][1],
#     domain_val=rows[0][2],
#     path_val=rows[0][3],
#     scraped_val=rows[0][4],
# )

# print (cur.execute(insert))

# conn.commit()

















# nope

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













