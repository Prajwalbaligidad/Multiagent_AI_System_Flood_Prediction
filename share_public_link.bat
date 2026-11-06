@echo off
title FloodGuard AI - Generate Public Share Link
color 0a
echo ===============================================================================
echo            FLOODGUARD AI: INSTANT PUBLIC INTERNET SHARING TUNNEL
echo ===============================================================================
echo.
echo  Creating a secure public HTTPS link for your dashboard (Port 5000)...
echo  Anyone in the world on any device or mobile phone will be able to open it!
echo.
echo  -------------------------------------------------------------------------------
echo   Press CTRL+C anytime to stop sharing.
echo  -------------------------------------------------------------------------------
echo.

npx localtunnel --port 5000
pause
