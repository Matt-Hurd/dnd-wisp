

from lxml import etree
import requests
from io import StringIO, BytesIO
from urllib.parse import urlparse, parse_qs
import psycopg2


def collect(row, cursor, db_conn):

    print (row)
    header_info = {'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}

    r = requests.get(row[1], headers=header_info, timeout=5)
    # r = requests.get("https://en.wikipedia.org/wiki/42_(school)", headers=header_info)

    # r = requests.get('https://gorails.com/', headers={'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"})
    # r = requests.get('http://www.imdb.com/')
    # r = requests.get('http://finofilipino.org/')
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

    
    

    


    framework_keys = ', '.join(found_frameworks)
    framework_values = ', '.join(["'1'"] * len(found_frameworks))

    meta_keys = ', '.join(found_metas.keys())
    meta_values = ', '.join(["'%s'" % x.replace("'", "\'") for x in found_metas.values()])


    links = tree.xpath("//a/@href")
    url_values = ""
    url_columns = "(url, domain, path, scraped, created_at, updated_at)"
    found_urls = set()
    for i, link in enumerate(links):
        parsed = urlparse(link)    
        if parsed.netloc:
            url = link.split('?')[0].split('#')[0]
            if (url[0] == '/' and url[1]== '/'):            
                url = url[2:]
            elif url[0] == '/':
                url = url[1:]         

            if not (url in found_urls):
                found_urls.add(url)
                if url_values == "":
                    url_values += "('{url_val}', '{domain_val}', '{path_val}', {scraped_val}, now(), now())".format(
                        url_val=url,
                        domain_val=parsed.netloc,
                        path_val=parsed.path,
                        scraped_val=False,                
                    )
                else:
                    url_values += ", ('{url_val}', '{domain_val}', '{path_val}', {scraped_val}, now(), now())".format(
                        url_val=url,
                        domain_val=parsed.netloc,
                        path_val=parsed.path,
                        scraped_val=False,                
                    )


    infa_columns = "url, domain, path, created_at, updated_at"
    infa_values = "'{url_val}', '{domain_val}', '{path_val}', now(), now()".format(
        url_val=row[1], domain_val=row[2], path_val=row[3], scraped_val=row[4]
    )

    join_columns = ', '.join(filter(None, [framework_keys, meta_keys, infa_columns]))
    join_values = ', '.join(filter(None, [framework_values, meta_values, infa_values]))

    scraped_columns = "({list})".format(list=join_columns)
    scraped_values = "({list})".format(list=join_values)

    if (url_values):
        print ("urls found: {found}".format(found=len(found_urls)))
        url_insert = "INSERT INTO urls {col} VALUES {val} ON CONFLICT (url) DO NOTHING;".format(col=url_columns, val=url_values)    
        cursor.execute(url_insert)
        db_conn.commit()
    if (framework_values or meta_values):
        scraped_insert = "INSERT INTO scraped_data {col} VALUES {val} ON CONFLICT (url) DO NOTHING;".format(col=scraped_columns, val=scraped_values)
        cursor.execute(scraped_insert)
        db_conn.commit()

    # for i, link in link_output:
    #     print ()
    #     print (link)
    #     insert_link


    # print ("\ninfa")
    # print (infa_columns)
    # print (infa_values)

    # print ("\nframework:")
    # print(framework_keys)
    # print(framework_values)

    # print ("\nmeta:")
    # print(meta_keys)
    # print(meta_values)

    # print ("\nurl:")
    # print (url_columns)
    # print (url_values)

    # print ("scraped_insert")
    # print (scraped_insert)

    # print ("url_insert")
    # print (url_insert)







conn = psycopg2.connect("dbname='dnd_database' user='postgres' host='138.197.194.84' password='a54fd22438e9e5892c0921405e339e19' port='26606'")


cur = conn.cursor()

lim = 10

distinct = "select distinct on (domain) * from urls where scraped = '0' limit {lim};".format(lim=lim)
update_scraped = "update urls set scraped='1' where {temp};"
q_reset_scraped = "update urls set scraped='0';"

cur.execute(distinct)
rows = cur.fetchall()

ids = ""
if (rows):
    for i, row in enumerate(rows):
        if (i == 0):
            ids = "id={idd}".format(idd=row[0])
        else:
            ids += "or id={idd}".format(idd=row[0])

            
    # print (update_scraped.format(temp=ids))
    cur.execute(update_scraped.format(temp=ids))
    conn.commit()

num_rows = len(rows)

print ("scraping: {len}".format(len=num_rows))
for i, row in enumerate(rows):
    try:
        print ("\nscraping-> {i}: {link}".format(i=i, link=row[1]))
        collect(row, cur, conn)
    except Exception as e:
        print ("\nbroke: {link}".format(i=i, link=row[1]))
        print ("{e}".format(e=e))





