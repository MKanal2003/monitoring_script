#!/bin/bash


echo "Making the application up"

nohup python3 -m http.server 8082 >> out.log 2>&1 &
