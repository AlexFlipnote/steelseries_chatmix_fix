@echo off
if not exist "%~dp0.venv\Scripts\Steelseries Fixer.exe" (
    copy /Y "%~dp0.venv\Scripts\pythonw.exe" "%~dp0.venv\Scripts\Steelseries Fixer.exe" >nul
)
start "" /B "%~dp0.venv\Scripts\Steelseries Fixer.exe" "%~dp0index.py"
