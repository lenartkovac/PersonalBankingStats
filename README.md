# PersonalBankingStats

A somewhat simple application that provides some statistics on spending, based on NKBM's csv financial statements

## Requirements

* nodeJS v16.8+
* docker v20+
* python v3.8+
* vue-cli v4.5+

## Installation Process

This section describes how you get started

## Clone

clone the repository to your local machine

### build project locally

in terminal, move to the root of repository and run

run `npm run init`

this command will:

* generate sample data
* install rquired npm module dependencies
* build vue project
* build server docker container
* download mongoDB container and link it to the server

### run project

in terminal run, from the root of the repository

run `npm run start`

this will start the server and database docker containers

### Stop/restart project

You can run the following commands from the repo root:

`npm run stop` stops the project completely. 

`npm run restart` which will stop the project, rebuild it and start it up again.
This is useful if you want to make some quick changes and restart the project in docker again.

## Implementation

This part describes the necessary steps to set up a local environment of the system for the purpose of additional implementation.
You can also follow these steps if you have issues setting up the application through docker or would just rather run it locally.

### ENV variables

Set up required environment variables

| VARIABLE NAME | DESCRIPTION | EXAMPLE VALUE  |
|---------------|-------------|---------------|
| DB_URL | url of mongodb database | 127.0.0.1 |
| DB_PORT | port of monodb database at the url | 27017 |
| FLASK_APP | location of the flask app | backend/app.py |
| FLASK_ENV | flask environment (production or development) | development |
| FLASK_RUN_PORT | port on which the server will be accessed | 8000 |
| DB_TIMEOUT_MS | db access timeout in ms | 10000 |
| DIST_PATH | path to the dist directory of Vue project (useful if you don't wish to run the Vue project separately) | ../frontend/bank-stats/dist |
| DATA_DIR | path to directory that hold the project data | ../data |

### Running process

to build the website run `npm buildWebsite`. This will download required npm modules and build the vue project.

run the server from the `app` directory using `flask run`. Server is available at `http://localhost:FLASK_RUN_PORT`

\*optional: run the vue project separatly from the bank-stats folder using `npm run serve`
