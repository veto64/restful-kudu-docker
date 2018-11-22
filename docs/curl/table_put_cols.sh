#!/bin/bash

curl -X PUT http://127.0.0.1/stock -d '{"cols":{"style":"string","qty":"int","hash":"string"}}'
