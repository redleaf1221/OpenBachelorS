pip install pyinstaller==6.11.1
pyinstaller -p . --contents-directory . --add-data conf:conf --add-data data:data --add-data res:res --add-data aria2c.exe:. main.py
pause
