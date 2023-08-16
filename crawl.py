import requests
import urllib.parse
import json
from json         import JSONDecodeError
from lib.utils    import log
from lib.utils    import load_settings
from lib.database import CrawlRequest
from lib.database import create_database_session

crawlbase_settings = load_settings()

crawlbase_js_token = crawlbase_settings.get('token')
crawlbase_crawler  = crawlbase_settings.get('crawler')

if crawlbase_js_token is None or crawlbase_js_token.strip() == '':
  print('--------------------------------------------------')
  print('Please set your Crawlbase token in the settings.yml')
  print('--------------------------------------------------')
  exit()

if crawlbase_crawler is None or crawlbase_crawler.strip() == '':
  print('-----------------------------------------------------')
  print('Please set your Crawlbase crawler in the settings.yml')
  print('-----------------------------------------------------')
  exit()

linked_in_profile_urls = open('urls.txt', 'r').readlines()

if len(linked_in_profile_urls) == 0:
  print('-----------------------------------------------------------------------------------------------------')
  print('There are no urls available. Please populate urls to `urls.txt` separated by new line.')
  print('-----------------------------------------------------------------------------------------------------')
  exit()

log('Starting crawling...')

crawlbase_api_url = 'https://api.crawlbase.com?token={0}&callback=true&crawler={1}&url={2}&autoparse=true'

session = create_database_session()

for url in linked_in_profile_urls:
  url = url.strip()
  encoded_url = urllib.parse.quote(url, safe='')
  api_url = crawlbase_api_url.format(crawlbase_js_token, crawlbase_crawler, encoded_url)

  log(f'Requesting to crawl {url}')

  try:
    response = requests.get(api_url)
    json_response = json.loads(response.text)
    crawlbase_rid = json_response['rid']
    crawl_request = CrawlRequest(url=url, crawlbase_rid=crawlbase_rid, status='waiting')
    session.add(crawl_request)
    session.commit()
  except JSONDecodeError:
    log(f'An error occured when decoding the json response\n{response.text}')
  except:
    log(f'Unknown error occured while crawling {url}')

log('Done crawling.')
