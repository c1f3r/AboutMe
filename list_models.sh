#!/bin/bash
_now=$(date +"%Y_%m_%d")
_file="static/$_now.dat"
chmod 777 static
echo "Starting write to $_file"
python manage.py list_models 2>> $_file
chmod 700 static