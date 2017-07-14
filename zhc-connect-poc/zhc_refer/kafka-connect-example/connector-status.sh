#! /bin/bash

## other commands
# check the status of the connector
curl -s -X GET http://localhost:8083/connectors/$1/status
