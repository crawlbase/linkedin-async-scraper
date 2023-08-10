# Introduction

  This is a app that crawls a list of LinkedIn Profiles using the reliable Crawlbase Crawler

# Signup to Crawlbase

  TODO:

  signup to crawlbase
  create a crawler
  get token

  Please visit the below link to enable LinkedIn crawling. 
  https://crawlbase.com/dashboard/account/domain/linkedin/agreement 

# File and Directory Structure

```
PROJECT_FOLDER
  data                            # Folder containing for Crawlbase Crawler returned data
  lib                             # Folder containing library related codes
    database.py                   # Database and ORM (Object-Relational-Mapping) related codes
    utils.py                      # Helper related codes
  callback_server.py              # Callback server scripts that handle Crawlbase Crawler callbacks
  crawl.py                        # Scripts that request crawling to Crawlbase from the list of urls
  linkedin_profile_urls.txt       # File that holds the list of urls to be crawled
  process.py                      # Scripts that process data returned from Crawlbase Crawler. It saves the linked in profile data to the database.
  README.md                       # This file
  requirements.txt                # Dependency needed by this app.
  settings.yml                    # File that holds our settings e.g. `token` and `crawler`.
```

# Installation

## Software Needed

1. Python 3
2. Mysql 8.0 and up
3. Ngrok

## Setup Mysql Database

  1. Create a user

```sql
CREATE USER 'linkedincrawler'@'localhost' IDENTIFIED BY 'linked1nS3cret';
```

  2. Create a database

```sql
CREATE DATABASE linkedin_crawler_db;
```

  3. Grant permission

```sql
GRANT ALL PRIVILEGES ON linkedin_crawler_db.* TO 'linkedincrawler'@'localhost';
```

  4. Set current database

```sql
USE linkedin_crawler_db;
```

  5. Create tables

```sql
CREATE TABLE IF NOT EXISTS `crawl_requests` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `url` TEXT NOT NULL,
  `status` VARCHAR(30) NOT NULL,
  `crawlbase_rid` VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS `linkedin_profiles` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `crawl_request_id` INT NOT NULL,
  `title` VARCHAR(255),
  `headline` VARCHAR(255),
  `summary` TEXT,

  FOREIGN KEY (`crawl_request_id`) REFERENCES `crawl_requests`(`id`)
);

CREATE TABLE IF NOT EXISTS `linkedin_profile_experiences` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `linkedin_profile_id` INT NOT NULL,
  `title` VARCHAR(255),
  `company_name` VARCHAR(255),
  `description` TEXT,
  `is_current` BIT NOT NULL DEFAULT 0,

  FOREIGN KEY (`linkedin_profile_id`) REFERENCES `linkedin_profiles`(`id`)
);
```

## Setup ngrok

See [ngrok Getting Started](https://ngrok.com/docs/getting-started/)

# Configuration

## Settings

In `settings.yml`, configure the `token` and `crawler` values on what you set in [Crawlbase Crawler](https://crawlbase.com/dashboard/crawler/crawlers)

Example:

```
# settings.yml
token: mynormalcrawlbasetoken
crawler: linkedin-profile-crawler
```

## List of URLs

Then make sure you have entries of urls in `linkedin_profile_urls.txt`.
Note that each line corresponds to a valid url. 
By default it is configured with 5 top [most followed people in LinkedIn](https://brigettehyacinth.com/top-20-most-followed-influencers-on-linkedi)

## Setup Python environment

  1. Create a virtual environment

```bash
$ python3 -m venv .venv
```

  2. Activate the virtual environment


```bash
$ . .venv/bin/activate
```

  3. Install dependencies


```bash
$ pip install -r requirements.txt
```

# Running

## I. Run the Crawler Callback Server

Start ngrok.

```bash
$ ngrok http 5000
```

Then run the callback server script.

```bash
$ python callback_server.py
```

Test the server

```bash
$ curl -i -X POST 'http://localhost:5000/crawlbase_crawler_callback' -H 'HTTP_RID: test'
```

If running normally then you should see a message in the console:

```
[app][2023-08-10 17:42:16] Callback server is working
```

Finally register the ngrok path to [Crawlbase Crawler dashboard](https://crawlbase.com/dashboard/crawler/crawlers)

Example:

```
https://ffb8-180-190-180-195.ngrok-free.app/crawlbase_crawler_callback
```

## II. Run the Processor

Open an new console with the same directory and activate

```bash
$ . .venv/bin/activate
```

Then run the processor

```bash
$ python process.py
```

This will keep on looping waiting for a data to be processed coming from Crawlbase.

## II. Initiate Crawling

Open an new console with the same directory and activate

```bash
$ . .venv/bin/activate
```

Then run the crawl script.

```bash
$ python crawl.py
```
