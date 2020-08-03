@echo off

git add . 

SET /P _inputname= commit message:

git commit -m "%_inputname%"

git push -f origin master 
