@echo off
set /p message="Enter commit message: "
python simple_setup.py --commit -m "%message%"
pause