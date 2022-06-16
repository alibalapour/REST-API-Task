# REST-API-Task
This repository provides a REST API by using fastapi with a simple HTML frontend. It consists of these functionalities:
* Get key-value items
* Set an Item with a versioned history
* Delete an Item with giving a key
* Update an Item with a key and value
* Fetch Item with a key
* Fetch history of an Item with a key

# How to use
After cloning the repository, you need to run the uvicorn server, and then, with opening your [local host](http://localhost:8000/) you can use the API.

```
# clone the repository
$ git clone https://github.com/alibalapour/REST-API-Task.git

# go the main directory of the repo
$ cd  REST-API-Task

# create and activate a virtual environment
$ python3 -m venv .env
$ source .env/bin/activate

# install the requirements
$ pip install -r requirements.txt

# run the server
$ uvicorn API.main:app --reload

# open your browser and go to http://localhost:8000
```
