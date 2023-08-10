import json
import sched
import time
from lib.utils    import log
from lib.utils    import is_iterable
from lib.database import CrawlRequest
from lib.database import LinkedinProfile
from lib.database import LinkedinProfileExperience
from lib.database import create_database_session

SCHEDULE_INTERVAL_IN_SECONDS = 60
RECORDS_COUNT_LIMIT_PER_PROCESSING = 10

session = create_database_session()

def process():
  received_crawl_requests = session.query(CrawlRequest).filter_by(status='received').limit(RECORDS_COUNT_LIMIT_PER_PROCESSING).all()

  if len(received_crawl_requests) == 0:
    log('No received crawl requests to process.')
  else:
    for crawl_request in received_crawl_requests:
      log(f'Processing Crawlbase rid {crawl_request.crawlbase_rid} with url {crawl_request.url}.')

      f = open(f'./data/{crawl_request.crawlbase_rid}.json')
      data = json.load(f)

      title = data.get('title')
      headline = data.get('headline')
      summaries = data.get('summary')
      summary = '\n'.join(summaries) if is_iterable(summaries) else None

      linkedin_profile = LinkedinProfile(title=title, headline=headline, summary=summary)
      linkedin_profile.crawl_request = crawl_request
      session.add(linkedin_profile)

      experiences = (data.get('experience') and data.get('experience').get('experienceList')) or []
      for experience in experiences:
        title = experience.get('title')
        company_name = experience.get('company') and experience.get('company').get('name')
        descriptions = experience.get('description')
        description = '\n'.join(descriptions) if is_iterable(descriptions) else None
        is_current = experience.get('currentPosition') == True

      linkedin_profile_experience = LinkedinProfileExperience(
          title=title,
          company_name=company_name,
          description=description,
          is_current=is_current
        )
      linkedin_profile_experience.linkedin_profile = linkedin_profile
      session.add(linkedin_profile_experience)

    crawl_request.status = 'processed'

    session.commit()

def process_and_reschedule():
  process()
  scheduler.enter(SCHEDULE_INTERVAL_IN_SECONDS, 1, process_and_reschedule)

if __name__ == '__main__':
  scheduler = sched.scheduler(time.monotonic, time.sleep)
  process_and_reschedule()
  scheduler.run()
