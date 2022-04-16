  # Cameron RV Park

## Description

A portal to manage RV Park bookings.

## Getting Started

Install the following dependencies:

* [Python 3.9.x](https://www.python.org/downloads/release/python-3910/)
* [Postgres 14.x](https://www.postgresql.org/download/)
* [Redis 6.x](https://redis.io/download)

To install python modules:
```
 pip install -r requirements.txt
```

## Commands

Create admin superuser
```
 python manage.py createsuperuser
```

Run database migrations
```
 python manage.py makemigrations
 python manage.py migrate
```

## Setup the following Config Vars on Heroku:
* ADMIN_USERNAME
* ADMIN_PASSWORD
* AWS_ACCESS_KEY_ID
* AWS_BUCKET_NAME
* AWS_HOME_METADATA_KEY
* AWS_REGION_NAME
* AWS_SECRET_ACCESS_KEY
* DATABASE_URL
* ENV_HOST
* DISABLE_COLLECTSTATIC

## Link to web-app:
https://cameron-rv-park.herokuapp.com/

## Authors
1. Alekhya Duba
2. Manik Taneja
3. Mudit Maheshwari
4. Rishabh Bhardwaj
5. Rohan Shah

