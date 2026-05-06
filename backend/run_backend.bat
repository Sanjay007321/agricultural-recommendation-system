@echo off
set "VIRTUAL_ENV="
set "PATH=%PATH:c:\SKS\crop\.venv\Scripts;=%"
cd c:\SKS\crop\backend
py -m venv venv4
call venv4\Scripts\activate.bat
pip install -r requirements.txt
python main.py
