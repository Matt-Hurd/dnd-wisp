

from lxml import etree
import requests
from io import StringIO, BytesIO
from urllib.parse import urlparse, parse_qs
# import psycopg2




# conn = psycopg2.connect("dbname='dnd_database' user='postgres' host='138.197.194.84' password='4339cc5bcd3dde693e9e96925014f71b' port='2619'")


# cur = conn.cursor()

# lim = 100

# distinct = "select distinct on (domain) * from urls limit {lim};".format(lim=lim)
# select = "select * from urls;"


# cur.execute(select)


    

# rows = cur.fetchall()



# print ("len: {l}".format(l=len(rows)))
# print (rows)


# # t.string   "url"
# # t.string   "domain"
# # t.string   "path"
# # t.boolean  "scraped"
# # t.integer  "counter"
# # t.datetime "created_at", null: false
# # t.datetime "updated_at", null: false
# # t.index ["url"], name: "index_urls_on_url", using: :btree



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

































# r = requests.get('https://gorails.com/')
# r = requests.get('https://paymentsplugin.com/demo/')
# r = requests.get('https://bugzilla.mozilla.org/')
r = requests.get('https://css-tricks.com/')

parser = etree.HTMLParser()


tree = etree.parse(StringIO(r.text), parser)

root = tree.getroot()








found_frameworks = set()

frameworks = {
    '//link/@href': {
        'bootstrap': 'bootstrap',
        'font_awesome': 'font-awesome',
        'google_font_api': 'fonts.google',
        'ionicons': 'ionicons',
        'lightbox': 'lightbox',
        'materialize_css': 'materialize',
        'outlook_web_app': '/themes/resources/owafont',
        'rdoc': 'rdoc-style.css'
    },
    "//input/@name": {
        'stripe': 'fullstripe',
        'django': 'csrfmiddlewaretoken',
        'infusionsoft': 'infusionsoft_version',
        'microsoft_asp_net': 'VIEWSTATE',
    },
    "//a/@href": {
        'bugzilla': 'enter_bug.cgi'
    },
    "//script": {
        'buy_sell_ads': 'bsa.src',
        'segment': 'segment.com/analytics',
        'spree': 'Spree.'
    },
}

for framework_type, items in frameworks.items():
    inputs = tree.xpath(framework_type)
    for i in inputs:
        if framework_type == '//script':
            i = i.text
            if not i:
                continue
        for key, value in items.items():
            if value in i:
                found_frameworks.add(key)

print(found_frameworks)



links = tree.xpath("//a/@href")
# head = root.xpath("//head")
# metas = root.xpath("//head/meta") 



# print (links)

# output = [{}]

# for i, link in enumerate(links):
#     parsed = urlparse(link)    
#     if parsed.netloc:
#         print("{i}: netloc: {v}".format(i=i, v=parsed.netloc))
#         print (parsed)
#         print ("url: {u}".format(u=link))
        # print ()







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













