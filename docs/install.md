# Installation

Currently, Programming Battle has only been tested and supported on Ubuntu Trusty.

## Step 1: set up the database

* Install postgres
* Create an empty databse
* Create a user who owns the database
* Enter the database connection string in your battle.yaml config

## Step 2: create programming battle folders

* /opt/progbattle which is owned by the user running the backend and frontend
* /opt/progbattle/runs which is world writable (this is where judging happens)
* /opt/progbattle/bin

## Step 3: setup isolate

* Setup Linux cgroups
* Compile isolate (make external/isolate)
* Move the isolate binary to /opt/progbattle/bin
* Make root the owner of the binary
* Make the binary setuid

## Step 4: Python dependencies

* Install the dependencies listed in battle/setup.py

## Step 5: running

* PYTHONPATH=battle:. ./scripts/start_web.py
* PYTHONPATH=battle:. ./scripts/start_daemon.py
