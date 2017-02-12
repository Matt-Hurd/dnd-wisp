from lxml import etree
import requests
from io import StringIO, BytesIO
from urllib.parse import urlparse, parse_qs
import psycopg2
import threading
import random


possible_frameworks = [
    'stripe',
    'bootstrap',
    'bugzilla',
    'buy_sell_ads',
    'carbon_ads',
    'disqus',
    'django',
    'dreamweaver',
    'drupal',
    'drupal_commerce',
    'font_awesome',
    'google_font_api',
    'google_tag_manager',
    'gravatar',
    'handlebars',
    'hubspot',
    'infusionsoft',
    'ionicons',
    'joomla',
    'kibana',
    'less',
    'lightbox',
    'magento',
    'mailchimp',
    'materialize_css',
    'meteor',
    'microsoft_asp_net',
    'open_web_analytics',
    'opencart',
    'outlook_web_app',
    'oracle_commerce',
    'oracle_commerce_cloud',
    'pdf_js',
    'paypal',
    'polymer',
    'pure_css',
    'pygments',
    'rdoc',
    'react',
    'reddit',
    'segment',
    'semantic_ui',
    'shopify',
    'spree',
    'syntax_highlighter',
    'tumblr',
    'vimeo',
    'woocommerce',
    'wordpress',
    'wordpress_super_cache',
    'yahoo_advertising',
    'yahoo_ecommerce',
    'yoast_seo',
    'youtube',
    'zurb_foundation',
    'c_panel',
]

possible_metas = [
    'keywords',
    'description',
    'author',
    'twitter_site',
    'twitter_title',
    'twitter_description',
    'twitter_image',
    'twitter_creator',
    'title',
    'h1',
    'og_title',
    'og_url',
    'og_description',
    'og_image',
    'og_site_name'
]

def collect(row, results, id):
    global possible, possible_frameworks
    #print (row)
    header_info = {'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}

    r = requests.head(row[1], headers=header_info, timeout=3)
    for key in r.headers.keys():
        if key.lower() == 'content-type' and not 'text/html' in r.headers[key]:
            #print(r.headers)
            return
    r = requests.get(row[1], headers=header_info, timeout=3)
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

    found_frameworks = {
        'stripe': '0',
        'bootstrap': '0',
        'bugzilla': '0',
        'buy_sell_ads': '0',
        'carbon_ads': '0',
        'disqus': '0',
        'django': '0',
        'dreamweaver': '0',
        'drupal': '0',
        'drupal_commerce': '0',
        'font_awesome': '0',
        'google_font_api': '0',
        'google_tag_manager': '0',
        'gravatar': '0',
        'handlebars': '0',
        'hubspot': '0',
        'infusionsoft': '0',
        'ionicons': '0',
        'joomla': '0',
        'kibana': '0',
        'less': '0',
        'lightbox': '0',
        'magento': '0',
        'mailchimp': '0',
        'materialize_css': '0',
        'meteor': '0',
        'microsoft_asp_net': '0',
        'open_web_analytics': '0',
        'opencart': '0',
        'outlook_web_app': '0',
        'oracle_commerce': '0',
        'oracle_commerce_cloud': '0',
        'pdf_js': '0',
        'paypal': '0',
        'polymer': '0',
        'pure_css': '0',
        'pygments': '0',
        'rdoc': '0',
        'react': '0',
        'reddit': '0',
        'segment': '0',
        'semantic_ui': '0',
        'shopify': '0',
        'spree': '0',
        'syntax_highlighter': '0',
        'tumblr': '0',
        'vimeo': '0',
        'woocommerce': '0',
        'wordpress': '0',
        'wordpress_super_cache': '0',
        'yahoo_advertising': '0',
        'yahoo_ecommerce': '0',
        'yoast_seo': '0',
        'youtube': '0',
        'zurb_foundation': '0',
        'c_panel': '0'
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
                    found_frameworks[key] = '1'

    # framework_str = " and ".join(["%s='1'" % (key) for key in found_frameworks])
    # #print(framework_keys)
    # #print(framework_values)
    # #print(found_frameworks)

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

    found_metas = {
        'keywords': None,
        'description': None,
        'author': None,
        'twitter_site': None,
        'twitter_title': None,
        'twitter_description': None,
        'twitter_image': None,
        'twitter_creator': None,
        'title': None,
        'h1': None,
        'og_title': None,
        'og_url': None,
        'og_description': None,
        'og_image': None,
        'og_site_name': None,
    }

    metas = root.xpath("//head/meta") 
    for meta in metas:
        if 'name' in meta.attrib.keys():
            if meta.attrib['name'] in names:
                found_metas[meta.attrib['name']] = meta.attrib['content']
        if 'property' in meta.attrib.keys():
            if meta.attrib['property'] in properties:
                found_metas[meta.attrib['property']] = meta.attrib['content']
    title = root.xpath("//head/title")
    for met in title:
        found_metas['title'] = met.text

    h1 = root.xpath("//h1[1]")
    for h in h1:
        found_metas['h1'] = h.text


    framework_values = ', '.join(["'%s'" % found_frameworks[x] for x in possible_frameworks])
    meta_values = ', '.join([("'%s'" % found_metas[x].replace("'", "''")) if found_metas[x] else "NULL" for x in possible_metas])


    links = tree.xpath("//a/@href")
    url_values = None
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
                if not url_values:
                    url_values = "('{url_val}', '{domain_val}', '{path_val}', {scraped_val}, now(), now())".format(
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

    infa_values = "'{url_val}', '{domain_val}', '{path_val}', now(), now()".format(
        url_val=row[1], domain_val=row[2], path_val=row[3], scraped_val=row[4]
    )
    join_values = ', '.join(filter(None, [framework_values, meta_values, infa_values]))
    scraped_values = "({list})".format(list=join_values)

    results[id] = (url_values, scraped_values)

conn = psycopg2.connect("dbname='dnd_database' user='postgres' host='138.197.194.84' password='a54fd22438e9e5892c0921405e339e19' port='26606'")


cur = conn.cursor()

lim = 32

while True:
    random_int = random.random() * (21474836 * random.random())        
    distinct = "select distinct on (domain) * from urls where scraped = '0' LIMIT {lim} OFFSET {offset};".format(lim=lim, offset=random_int)
    update_scraped = "update urls set scraped='1' where {temp};"
    q_reset_scraped = "update urls set scraped='0';"

    cur.execute(distinct)
    rows = cur.fetchall()

    threads = [None] * lim
    results = [None] * lim
    ids = ""
    if (rows):
        for i, row in enumerate(rows):
            if (i == 0):
                ids = "id={idd}".format(idd=row[0])
            else:
                ids += "or id={idd}".format(idd=row[0])

                
        # #print (update_scraped.format(temp=ids))
        cur.execute(update_scraped.format(temp=ids))
        conn.commit()

    num_rows = len(rows)

    # #print ("scraping: {len}".format(len=num_rows))
    url_values = []
    scraped_values = []
    for i, row in enumerate(rows):
        try:
            print ("\nscraping-> {i}: {link}".format(i=i, link=row[1]))
            # threads[i] = threading.Thread(target=collect, args = (row, results, i))
            # threads[i].daemon = True
            # threads[i].start()
            collect(row, results, i)
        except Exception as e:
            # pass
            print ("\nbroke: {link}".format(i=i, link=row[1]))
            print ("{e}".format(e=e))
    # for t in threads:
    #     t.join()
    for result in filter(None, results):
        url_values.append(result[0])
        scraped_values.append(result[1])
    url_values = ", ".join(filter(None, url_values))
    scraped_values = ", ".join(filter(None, scraped_values))


    framework_keys = ', '.join(possible_frameworks)
    meta_keys = ', '.join(possible_metas)
    infa_columns = "url, domain, path, created_at, updated_at"
    join_columns = ', '.join(filter(None, [framework_keys, meta_keys, infa_columns]))
    scraped_columns = "({list})".format(list=join_columns)
    url_columns = "(url, domain, path, scraped, created_at, updated_at)"
    if (url_values):
        # #print ("urls found: {found}".format(found=len(found_urls)))
        url_insert = "INSERT INTO urls {col} VALUES {val} ON CONFLICT (url) DO NOTHING;".format(col=url_columns, val=url_values)    
        cur.execute(url_insert)
        conn.commit()
    if (scraped_values):
        scraped_insert = "INSERT INTO scraped_data {col} VALUES {val} ON CONFLICT (url) DO NOTHING;".format(col=scraped_columns, val=scraped_values)
        cur.execute(scraped_insert)
        conn.commit()
