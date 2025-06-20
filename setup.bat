@echo off
echo.
echo GitHub Setup
echo ============
echo.

python simple_setup.py --setup

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Setup complete!
    echo.
    echo Quick commands:
    echo   - Commit: python simple_setup.py --commit -m "Your message"
    echo   - Status: git status
    echo   - Push: git push
    echo.
) else (
    echo.
    echo Setup failed!
)

pause