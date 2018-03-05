# Papusa
[![Build Status](https://travis-ci.org/karimtabet/papusa.svg?branch=master)](https://travis-ci.org/karimtabet/papusa)

Generic CMS Built with Django and Wagtail

## Getting Started
Clone the repository and enter it's directory:
```
git clone git@github.com:karimtabet/papusa.git && cd papus
```
Initialise and activate a virtualenv:
```
virtualenv -p python3 env && source env/bin/activate
```

Install dependencies:
```
pip install -r requirements.txt
```
Set your `SECRET_KEY` variable:
```
export SECRET_KEY=some_secret
```
Set up your database into a `db.sqlite3` file:
```
python manage.py migrate
```
Load  some dummy data:
```
python manage.py loaddata app/fixtures/demo.json
```
Start the server:
```
python manage.py runserver
```
Your server should now be running on port `8000`. Visit http://127.0.0.1:8000/ in your browser.

Access the admin panel by visitin http://127.0.0.1:8000/admin/.

A default admin user is set up with credentials **admin:admin**.

