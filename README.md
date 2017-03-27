<p align="center"><img src="https://raw.githubusercontent.com/rit-sailing/website/master/main/static/assets/images/logo.png" width="200"></p>
# RISC Website
The is the website created for the RISC club.
It is written in python and uses a framework called [Django](https://www.djangoproject.com/)

## Requirements
This project requires [python](https://www.python.org/downloads/) to run (can be 2 or 3).

## Setup
After you clone the repo please run the following commands to install the dependencies.
```bash
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py loaddata data.json
```
#### Troubleshooting
If you do not have pip installed with python grab it [here](https://pip.pypa.io/en/stable/installing/).

## Usage
To run the site, just enter the following command:
```bash
$ python manage.py runserver
```
This should start a development server on you machine on the port 8000.
To view the site just goto [localhost:8000](http://localhost:8000/).

The admin panel is located at [/admin](http://localhost:8000/admin/).
To log in use these credentials:
```
username: admin
password: thisisapass
```

## Issues and Feature Requests
Please submit all bugs, issues and feature requests in the issues section of the github repo.

## Task Management
We are using Taiga to do our task management. [Check out our board](https://tree.taiga.io/project/gdaunton-rit-sailing-website) to see what we are up to!

## Pull Requests
We do accept and look through pull requests. If you have a feature or fix send it our way!
