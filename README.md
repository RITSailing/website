# RIT Sailing Website
The is the website created for the RIT Sailing club
It is written in javascript and uses a framework called [keystone.js](http://keystonejs.com/)

## Requirements
This project requires [node.js](https://nodejs.org/en/download/) and [mongodb](https://www.mongodb.org/downloads#production) to run.

## Setup
After you clone the repo please run the following commands to install the dependencies.
```bash
$ npm install
$ mkdir data
```
Also in order for the project to run you need to download the [.env file](https://drive.google.com/a/g.rit.edu/file/d/0B3XhKKD9_3WmWXV2ejJkRm41bDg/view?usp=sharing) and place it in the root of the project.

## Usage
To run the site, just enter the following commands in **two separate command windows**:
```bash
$ mongod -dbpath data
$ node keystone
```
This should start a development server on you machine on the port 3000.
To view the site just goto [localhost:3000](http://localhost:3000/).

The admin panel for keystone is located at [/keystone](localhost:3000/keystone).
To log in use these credentials:
```
username: admin@admin.com
password: pass
```

## Issues and Feature Requests
Please submit all bugs, issues and feature requests in the issues section of the github repo.

## Task Management
We are using Taiga to do our task management. [Check out our board](https://tree.taiga.io/project/gdaunton-rit-sailing-website) to see what we are up to!

## Pull Requests
We do accept and look through pull requests. If you have a feature or fix send it our way!
