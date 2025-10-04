@echo off
echo ================================================
echo        REVISION SCHEDULE MANAGER
echo ================================================
echo.
echo This program helps you track study topics and
echo automatically schedules revisions using spaced
echo repetition principles.
echo.
echo REVISION INTERVALS:
echo - 1st revision: 1 day after learning
echo - 2nd revision: 7 days after 1st revision
echo - 3rd revision: 15 days after 2nd revision
echo - 4th revision: 1 month after 3rd revision
echo - 5th revision: 3 months after 4th revision
echo - 6th revision: 6 months after 5th revision
echo.
echo REQUIREMENTS:
echo - Python 3.6 or higher
echo - pandas library (for Excel export)
echo - openpyxl library (for Excel export)
echo.
echo TO INSTALL REQUIREMENTS:
echo   python -m pip install pandas openpyxl
echo.
echo TO RUN THE PROGRAM:
echo   python revision_scheduler.py
echo.
pause