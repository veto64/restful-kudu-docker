#!/bin/bash

curl -X PUT http://127.0.0.1/stock3 -d '{"style":"string","qty":"int","cost":"float","price":"float","hash":"string"}'
