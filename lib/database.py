from typing         import List
from sqlalchemy     import ForeignKey
from sqlalchemy     import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
  pass

class CrawlRequest(Base):
  __tablename__ = 'crawl_requests'

  id: Mapped[int] = mapped_column(primary_key=True)
  url: Mapped[str]
  status: Mapped[str]
  crawlbase_rid: Mapped[str]
  linkedin_profile: Mapped['LinkedinProfile'] = relationship(back_populates='crawl_request')

class LinkedinProfile(Base):
  __tablename__ = 'linkedin_profiles'

  id: Mapped[int] = mapped_column(primary_key=True)
  title: Mapped[str]
  headline: Mapped[str]
  summary: Mapped[str]
  crawl_request_id: Mapped[int] = mapped_column(ForeignKey('crawl_requests.id'))
  crawl_request: Mapped['CrawlRequest'] = relationship(back_populates='linkedin_profile')
  experiences: Mapped[List['LinkedinProfileExperience']] = relationship(back_populates='linkedin_profile')

class LinkedinProfileExperience(Base):
  __tablename__ = 'linkedin_profile_experiences'

  id: Mapped[int] = mapped_column(primary_key=True)
  title: Mapped[str]
  company_name: Mapped[str]
  description: Mapped[str]
  is_current: Mapped[bool]
  linkedin_profile_id: Mapped[int] = mapped_column(ForeignKey('linkedin_profiles.id'))
  linkedin_profile: Mapped['LinkedinProfile'] = relationship(back_populates='experiences')

def create_database_session():
  connection_string = 'mysql+mysqlconnector://linkedincrawler:linked1nS3cret@localhost:3306/linkedin_crawler_db'
  engine = create_engine(connection_string, echo=True)
  return Session(engine)
