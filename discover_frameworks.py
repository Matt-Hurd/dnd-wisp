

from lxml import etree
import requests
from io import StringIO, BytesIO
from urllib.parse import urlparse, parse_qs
header_info = {'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
# r = requests.get('https://gorails.com/', headers={'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"})
# r = requests.get('http://www.imdb.com/')
r = requests.get('http://finofilipino.org/')
# r = requests.get('http://www.sephora.com/')
# r = requests.get('https://paymentsplugin.com/demo/')
# r = requests.get('https://bugzilla.mozilla.org/')
# r = requests.get('https://css-tricks.com/', headers=header_info)

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
        'rdoc': 'rdoc-style.css',
        'wordpress': 'wp-'
    },
    "//input/@name": {
        'stripe': 'fullstripe',
        'django': 'csrfmiddlewaretoken',
        'infusionsoft': 'infusionsoft_version',
        'microsoft_asp_net': 'VIEWSTATE',
        'oracle_commerce': '_dyncharset'
    },
    "//a/@href": {
        'bugzilla': 'enter_bug.cgi'
    },
    "//script": {
        'buy_sell_ads': 'bsa.src',
        'segment': 'segment.com/analytics',
        'spree': 'Spree.'
    },
    "//input/@value": {
        'paypal': '_s-xclick'
    },
    "//iframe/@src": {
        'tumblr': 'tumblr.com'
    },
    "//a": {
        'reddit': 'Powered by Reddit'
    }
}

for framework_type, items in frameworks.items():
    inputs = tree.xpath(framework_type)
    for i in inputs:
        if not '@' in framework_type:
            i = i.text
            if not i:
                continue
        for key, value in items.items():
            if value in i:
                found_frameworks.add(key)

# framework_str = " and ".join(["%s='1'" % (key) for key in found_frameworks])
# print(framework_keys)
# print(framework_values)
# print(found_frameworks)

names = [
    'keywords',
    'description',
    'author',
    'twitter_site',
    'twitter_title',
    'twitter_description',
    'twitter_image',
    'twitter_creator',
]

properties = [
    'og_title',
    'og_url',
    'og_description',
    'og_image',
    'og_site_name',
]

found_metas = {}

metas = root.xpath("//head/meta") 
for meta in metas:
    if 'name' in meta.attrib.keys():
        if meta.attrib['name'] in names:
            found_metas[meta.attrib['name']] = meta.attrib['content']
    if 'property' in meta.attrib.keys():
        if meta.attrib['property'] in properties:
            found_metas[meta.attrib['property']] = meta.attrib['content']


framework_keys = ','.join(found_frameworks)
framework_values = ','.join(["'1'"] * len(found_frameworks))

meta_keys = ','.join(found_metas.keys())
meta_values = ','.join(["'%s'" % x for x in found_metas.values()])

print(framework_keys)
print(framework_values)
print(meta_keys)
print(meta_values)

# meta_str = " and ".join(["%s='%s'" % (key, val) for key, val in found_metas.items()])


# print(framework_str, "and", meta_str)