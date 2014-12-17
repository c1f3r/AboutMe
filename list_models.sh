#!/bin/bash
_now=$(date +"%Y_%m_%d")
_dir="."
_cp_dir="uploads"
_file="$_dir/$_now.dat"
_cp_file="$_cp_dir/$_now.dat"
chmod 777 $_dir $_cp_dir
echo "Starting write to $_file"
python manage.py list_models 2>> $_file
cp $_file $_cp_file
chmod 700 $_dir $_cp_dir