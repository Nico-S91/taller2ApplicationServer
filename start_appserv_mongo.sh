#!/bin/bash
docker run --name appserv --link some-mongo:mongo --rm -e MONGODB_URI=mongo -p 5000:5000 -p 8000:8000 appserv

