@echo off
echo Installing EsoFur...

set SCRIPT_DIR=%~dp0

:: Wrapper for Command Prompt
(
    echo @echo off
    echo python "%SCRIPT_DIR%esofur" %%*
) > "%SCRIPT_DIR%esofur.bat"

:: Wrapper for PowerShell / VS Code
(
    echo python "%SCRIPT_DIR%esofur" $args
) > "%SCRIPT_DIR%esofur.ps1"

:: Add project folder to PATH permanently
setx PATH "%PATH%;%SCRIPT_DIR%"

echo Installed successfully!
echo Restart your terminal or VS Code for PATH changes to take effect.
echo Try: esofur run test.EsoFur
