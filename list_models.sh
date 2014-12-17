#!/bin/bash
_now=$(date +"%Y_%m_%d")
_dir="assets"
_file="$_dir/$_now.dat"
chmod 777 $_dir
echo "Starting write to $_file"
python manage.py list_models 2>> $_file
chmod 700 $_dir