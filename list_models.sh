#!/bin/bash
_now=$(date +"%Y_%m_%d")
_file="$_now.dat"
#chmod 777 .
echo "Starting write to $_file"
python manage.py list_models 2>> $_file
#chmod 700 .