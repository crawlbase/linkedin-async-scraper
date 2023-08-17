# Introduction

  This code is an accompaniment for [Full Guide: Creating Flask Callback Server to Store LinkedIn Profiles in MySQL using Crawlbase Crawler](https://crawlbase.com/blog/flask-callback-server-linkedin-mysql-crawlbase) blog.



# Getting Started

## Software Needed

1. [Python 3](https://www.python.org/)
2. [MySQL 8.0 or higher version](https://dev.mysql.com/downloads/mysql/)
3. [Ngrok](https://ngrok.com/docs/getting-started/)

## Setup MySQL Database Schema

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
CREATE INDEX `idx_crawl_requests_status` ON `crawl_requests` (`status`);
CREATE INDEX `idx_crawl_requests_crawlbase_rid` ON `crawl_requests` (`crawlbase_rid`);
CREATE INDEX `idx_crawl_requests_status_crawlbase_rid` ON `crawl_requests` (`status`, `crawlbase_rid`);

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

## Settings

In `PROJECT_FOLDER/settings.yml`, configure the `token` and `crawler` values on what you set in [Crawlbase Crawler](https://crawlbase.com/dashboard/crawler/crawlers)

Example:

```
# PROJECT_FOLDER/settings.yml
token: mynormalcrawlbasetoken
crawler: linkedin-profile-crawler
```

## List of URLs

Then make sure you have entries of urls in `PROJECT_FOLDER/urls.txt`.
Note that each line corresponds to a valid url. 
By default it is configured with 5 top [most followed people in LinkedIn](https://brigettehyacinth.com/top-20-most-followed-influencers-on-linkedi)

## Setup Python Virtual Environment

### 1. Create a virtual environment in our project folder

```bash
PROJECT_FOLDER$ python3 -m venv .venv
```

### 2. Activate the virtual environment


```bash
PROJECT_FOLDER$ . .venv/bin/activate
```

### 3. Install dependencies


```bash
PROJECT_FOLDER$ pip install -r requirements.txt
```

## I. Running the Crawler Callback Server

### 1. Start ngrok.

Open a new terminal and run the command below:

```bash
$ ngrok http 5000
```

Then remember the forwarding url that looks like below:

```
Forwarding                    https://4e15-180-190-160-114.ngrok-free.app -> http://localhost:5000
```

What we need is the `https://4e15-180-190-160-114.ngrok-free.app` value and we will use this later.

### 2. Then run the callback server script.

Open a new terminal and run the command below to activate the python virtual environment for this terminal

```bash
PROJECT_FOLDER$ . .venv/bin/activate
```
Then run the callback server

```bash
PROJECT_FOLDER$ python callback_server.py
```

### 3. Test the server

On a new terminal, run the following:

```bash
$ curl -i -X POST 'http://localhost:5000/crawlbase_crawler_callback' -H 'RID: dummyrequest' -H 'Accept: application/json' -H 'Content-Type: gzip/json' -H 'User-Agent: Crawlbase Monitoring Bot 1.0' -H 'Content-Encoding: gzip' --data-binary '"\x1F\x8B\b\x00+\xBA\x05d\x00\x03\xABV*\xCALQ\xB2RJ)\xCD\xCD\xAD,J-,M-.Q\xD2QJ\xCAO\xA9\x04\x8A*\xD5\x02\x00L\x06\xB1\xA7 \x00\x00\x00' --compressed
```

If running normally then you should see a message in the console:

```
[app][2023-08-10 17:42:16] Callback server is working
```

### 4. Finally register the ngrok path to [Crawlbase Crawler dashboard](https://crawlbase.com/dashboard/crawler/crawlers)

Example:

```
https://4e15-180-190-160-114.ngrok-free.app/crawlbase_crawler_callback
```

## II. Runing the Periodic Processor

Open a new terminal and run the command below to activate the python virtual environment for this terminal

```bash
PROJECT_FOLDER$ . .venv/bin/activate
```

Then run the processor

```bash
PROJECT_FOLDER$ python process.py
```

This will keep on looping and waiting for a data to be processed coming from Crawlbase.

## III. Initiating Crawling

Open a new terminal and run the command below to activate the python virtual environment for this terminal

```bash
PROJECT_FOLDER$ . .venv/bin/activate
```

Then run the crawl script.

```bash
PROJECT_FOLDER$ python crawl.py
```
