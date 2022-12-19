# Policy Design Lab API
API service for Policy Design Lab

## Configuration Guide

### Pre-requisites
- Python 3.8 or higher
- Install poetry: `pip install poetry`

## Setup and Run 

### Local Run
Set packages:
`poetry lock`

Install packages:
`poetry install`

Set variables:
- for local run you have to be connected to the database
- create .env file under pdl-api/api/controllers folder. 
- The content of .env file should be like

      DB_HOST=host machine
      DB_PORT=5432
      DB_NAME=pdl
      DB_USERNAME=username
      DB_PASSWORD=password`

Change directory into pdl-api/app 
`python main.py`

Now you can view the API at http://localhost:5000/pdl/

For swagger doc, go to http://localhost:5000/ui

### Using Docker
Create the PDL API Docker image and run the Docker container:
        
      docker build -t pdl/pdl-api .
      docker run -p 80:5000 pdl/pdl-api 

Now you can view the API at http://localhost/pdl/

For swagger doc, go to http://localhost/ui


