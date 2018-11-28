#!/bin/bash 

<<EOF

bash examples:
./create.sh stock '{"style":"string","qty":"int","cost":"float","price":"float","weight":"float","date","int","hash":"string"}'

curl examples:
curl -X PUT http://127.0.0.1/stock
curl -X PUT http://127.0.0.1/stock3 -d '{"style":"string","qty":"int","cost":"float","price":"float","hash":"string"}'

EOF


if [ -z $1 ] 
then 
  echo "Missing table parameter"
  exit
else 
 table=$1
fi

if [ -z $2 ] 
then 
  echo "Missing col parameter"
  exit
else 
 cols=$2
fi


echo "create database ${table} with ${cols}"

curl -X PUT http://127.0.0.1/${table} -d ${cols}
