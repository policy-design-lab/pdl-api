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
- create .env file under pdl-api/app/controllers folder. 
- The content of .env file should be like

      DB_HOST=host machine
      DB_PORT=5432
      DB_NAME=pdl
      DB_USERNAME=username
      DB_PASSWORD=password
      API_PORT=API port, default 5000 if not set

Change directory into pdl-api/app 
`python main.py`

Now you can view the API at http://localhost:{API_PORT}/pdl/

For swagger doc, go to http://localhost:{API_PORT}/ui

### Using Docker
Create the PDL API Docker image and run the Docker container:
        
      docker build -t pdl/pdl-api .
      docker run -e DB_HOST=db_host -e DB_PORT=5432 -e DB_NAME=pdl -e DB_USERNAME=username -e DB_PASSWORD=password -e API_PORT=port -p port:port pdl/pdl-api 

Now you can view the API at http://localhost/pdl/

For swagger doc, go to http://localhost/ui

## Short note on total payment calculation
When calculating the total dollar amounts payment calculation, the following details are considered in the GET /pdl/allprograms endpoint:
1. In CRP, the "Total CRP" sub program contains the total value of all CRP payments. Just for the purpose of calculating the total values, the other sub programs and sub-sub programs in that can be ignored.
2. In Crop Insurance, the column `net_farmer_benefits_amount` contain the amount value that should be used for the total payment calculation. The `payment` column value is NULL for that program.
