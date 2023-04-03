# movie-picker
Web App for storing movie lists and picking a movie to watch based on preferences

# How to use
1. Install requirements: 
flask, flask-bootstrap, flask-sqlalchemy, requests, waitress


2. Set environment variables. 
This program relies on registry with flask. To find yours


3. To run: 
waitress-serve --host 127.0.0.1 main:app


To make a Desktop shortcut for easy use: 

1. Need to allow permission for running ps1 files
# set permission to run: Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
2. CHange the ps1 script for your environment variables. 
3. Desktop --> create shortcut and type "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -noexit  -ExecutionPolicy Bypass C:/path/to/run.ps1"
