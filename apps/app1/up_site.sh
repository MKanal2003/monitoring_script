#!/bin/bash 

echo "Making the application up"


nohup python3 -m http.server 8081 >> out.log 2>&1 &


