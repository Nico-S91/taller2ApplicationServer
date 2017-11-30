#!/bin/bash
docker run --name appserv --link some-mongo:mongo --link sserv:sserv --rm -e MONGODB_URI=mongo -e SHARED_SERVER_URL=http://sserv:5001 -p 5000:5000 -p 8000:8000 appserv
