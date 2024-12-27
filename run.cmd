call venv\Scripts\activate.bat
waitress-serve --host=127.0.0.1 --port=8443 src.app:app
pause
