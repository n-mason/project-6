# UOCIS322 - Project 6 #

## Name: Nathaniel Mason

## Contact Info: nmason@uoregon.edu

## Project Description:
The goal of this project is to add RESTful API that will work with the web application (the brevet time calculator) and MongoDB. The web app contains two buttons that will call the RESTful API which will submit data or retrieve data from the MongoDB database.
* The application is a worksheet on the web that allows the user to choose a distance and start date, and then after entering the distance value of a brevet controle, the opening and closing time of the controle will be displayed
* The algorithm is based on the algorithm from the RUSA website, which can be found at: https://rusa.org/pages/acp-brevet-control-times-calculator
* There are two buttons: Submit and Display, which call the RESTful API
* The user can use the Display and Submit buttons to call GET and POST through the brevets resource, and curl to test the other RESTful API services that use the brevet resource (and an ID). The services are the following:
    * GET http://API:PORT/api/brevets will display all brevets stored in the database.
    * GET http://API:PORT/api/brevet/ID will display brevet with id ID.
    * POST http://API:PORT/api/brevets will insert brevet object in request into the database.
    * DELETE http://API:PORT/api/brevet/ID will delete brevet with id ID.
    * PUT http://API:PORT/api/brevet/ID will update brevet with id ID with object in request.

### To start the application, the user should use the following docker commands:
* "docker compose up" to build your images and get the containers running
* Then, go to "localhost:5002" to view the brevet time calculator

#### Basically, with this updated version of the the code from Project 5, we now have the brevet calculator as the front-end on the web, and the RESTful API on the back-end (and the API is what communicates with MongoDB). 
