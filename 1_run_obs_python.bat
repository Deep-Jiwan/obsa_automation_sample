cd C:\"Program Files"\obs-studio\bin\64bit
start obs64.exe

timeout -t 10

cd C:\path\to\script
python obsrun.py

timeout -t 5
taskkill/F /IM obs64.exe