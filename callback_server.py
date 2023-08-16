import gzip
from flask        import Flask
from flask        import jsonify
from flask        import request
from lib.utils    import log
from lib.database import CrawlRequest
from lib.database import create_database_session

app = Flask(__name__)
session = create_database_session()

@app.route('/crawlbase_crawler_callback', methods=['POST'])
def crawlbase_crawler_callback():
  crawlbase_rid = request.headers.get('rid')
  content_encoding = request.headers.get('Content-Encoding')
  original_status = request.headers.get('Original-Status')
  if (not original_status is None):
    original_status = int(original_status.split(',')[0])
  crawlbase_status = request.headers.get('PC-Status')
  if (not crawlbase_status is None):
    crawlbase_status = int(crawlbase_status.split(',')[0])

  if crawlbase_rid is None:
    log(f'Crawlbase rid is not set.')
    return ('', 204)

  if crawlbase_rid == 'dummyrequest':
    log('Callback server is working')
    return ('', 204)

  if crawlbase_status != 200:
    log(f'Crawlbase status is not 200.')
    return ('', 204)

  if original_status != 200:
    log(f'Original status is not 200.')
    return ('', 204)

  crawl_request_does_not_exist = session.query(CrawlRequest).filter_by(crawlbase_rid=crawlbase_rid, status='waiting').first() is None

  if crawl_request_does_not_exist:
    log(f'No Crawlbase rid {crawlbase_rid} found with status `waiting`.')
    return ('', 204)

  crawl_request = session.query(CrawlRequest).filter_by(crawlbase_rid=crawlbase_rid, status='waiting').scalar()

  body = request.data
  if content_encoding == 'gzip':
    try:
      body = gzip.decompress(body)
    except OSError:
      pass

  with open(f'./data/{crawlbase_rid}.json', 'wb') as f:
    f.write(body)
  
  crawl_request.status = 'received'
  session.commit()

  log(f'Crawlbase rid {crawlbase_rid} was successfully received.')

  return ('', 201)

if __name__ == '__main__':
  app.run()
