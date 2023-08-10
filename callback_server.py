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
  crawlbase_rid = request.headers.get('HTTP_RID')

  if crawlbase_rid is None:
    log(f'Crawlbase rid is not set.')
    return ('', 204)

  if crawlbase_rid == 'test':
    log('Callback server is working')
    return ('', 204)

  crawl_request_does_not_exist = session.query(CrawlRequest).filter_by(crawlbase_rid=crawlbase_rid).first() is None

  if crawl_request_does_not_exist:
    log(f'Crawlbase rid {crawlbase_rid} does not exist in the database.')
    return ('', 204)

  crawl_request = session.query(CrawlRequest).filter_by(crawlbase_rid = crawlbase_rid).scalar()

  if crawl_request.status != 'waiting':
    log(f'Crawlbase rid {crawlbase_rid} might have been already processed.')
    return ('', 204)

  data = gzip.decompress(request.data)
  with open(f'./data/{crawlbase_rid}.json', 'wb') as f:
    f.write(data)
  
  crawl_request.status = 'received'
  session.commit()

  log(f'Crawlbase rid {crawlbase_rid} was successfully processed.')

  return ('', 201)

if __name__ == '__main__':
  app.run()
