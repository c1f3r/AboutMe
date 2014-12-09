#!/bin/bash
_now=$(date +"%Y_%m_%d")
_file="$_now.dat"
echo "Starting write to $_file"
python manage.py list_models 2>> $_file