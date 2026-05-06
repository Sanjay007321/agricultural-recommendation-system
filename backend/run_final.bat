@echo off
set VIRTUAL_ENV=
py -m venv c:\SKS\crop\backend\venv_final
c:\SKS\crop\backend\venv_final\Scripts\python.exe -m pip install -r c:\SKS\crop\backend\requirements.txt
c:\SKS\crop\backend\venv_final\Scripts\python.exe c:\SKS\crop\backend\main.py
