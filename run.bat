echo "Hello World!!!"
cd /D "%~dp0"
python -m flask --app app --debug run
pause