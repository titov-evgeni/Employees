<h1 align="center">Employee Project</h1>

## Description
REST API for directory of employees application

## Run the application
#### Run docker compose

    docker-compose up --build

#### Run command to automatically fill the database

In a `new terminal`, write command to use Seeder:
    
    docker-compose exec web python manage.py seed
Or write command to use database script:
    
    docker-compose exec web python manage.py db_script
Use `--mode=clear` to clear all data without filling the database
    
    docker-compose exec web python manage.py seed --mode=clear

    Or
    
    docker-compose exec web python manage.py db_script --mode=clear
####Add permission group for the application
Create a `group` through the `Admin panel` with the name of the `API Access` and specify this group to user in order to access the API
