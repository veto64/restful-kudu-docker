#!/bin/bash

if [ -z $1 ] 
then 
  echo "Missing table parameter"
else 
  curl -X DELETE http://127.0.0.1/${1}
fi




