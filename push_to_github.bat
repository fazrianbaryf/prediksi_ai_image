@echo off
setlocal

echo Checking for Git...

REM Attempt 1: Check if git is in PATH
git --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Git found in PATH!
    goto :FOUND_PATH
)

REM Attempt 2: Check standard Install locations
if exist "C:\Program Files\Git\cmd\git.exe" (
    set "GIT_PATH=C:\Program Files\Git\cmd\git.exe"
    echo Git found at default location.
    goto :FOUND_EXE
)

if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Git\cmd\git.exe" (
    set "GIT_PATH=C:\Users\%USERNAME%\AppData\Local\Programs\Git\cmd\git.exe"
    echo Git found at user location.
    goto :FOUND_EXE
)

REM Attempt 3: Ask User
echo.
echo ----------------------------------------------------------------------
echo ERROR: Could not find Git automatically.
echo ----------------------------------------------------------------------
echo If you just installed it, you might need to RESTART YOUR COMPUTER
echo for the settings to take effect.
echo.
echo OR, if you know where git.exe is, paste the full path below.
echo (Example: D:\Apps\Git\cmd\git.exe)
echo.
set /p GIT_PATH="path to git.exe: "

if not exist "%GIT_PATH%" (
    echo.
    echo Still cannot find git at: "%GIT_PATH%"
    echo Please restart your computer and try again.
    pause
    exit /b
)

:FOUND_EXE
REM Run via full path
echo.
echo Using Git at: "%GIT_PATH%"
echo Initializing Git repository...
"%GIT_PATH%" init
"%GIT_PATH%" add .
"%GIT_PATH%" commit -m "Initial commit for AI vs Human Art Check App"
"%GIT_PATH%" remote add origin https://github.com/fazrianbaryf/prediksi_ai_image.git
"%GIT_PATH%" branch -M main
"%GIT_PATH%" push -u origin main
echo Done!
pause
exit /b

:FOUND_PATH
REM Run via PATH
echo Initializing Git repository...
git init
git add .
git commit -m "Initial commit for AI vs Human Art Check App"
git remote add origin https://github.com/fazrianbaryf/prediksi_ai_image.git
git branch -M main
git push -u origin main
echo Done!
pause
