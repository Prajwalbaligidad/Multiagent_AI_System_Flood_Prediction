@echo off
title FloodGuard AI - Citizen Disaster Early Warning Dashboard
color 0b
echo ===============================================================================
echo            FLOODGUARD AI: NATIONAL EARLY WARNING CITIZEN DASHBOARD
echo            Autonomous Multi-Agent AI System & Live Geospatial Portal
echo ===============================================================================
echo.
echo  [1] Starting Local Multi-Agent Flask Web Server...
echo  [2] Connecting Live Open-Meteo Weather & GloFAS Hydrological Feed...
echo  [3] Initializing 4 Specialist AI Agents (Weather, Flood, Terrain, Satellite)...
echo.
echo  -------------------------------------------------------------------------------
echo   Web Dashboard URL: http://127.0.0.1:5000
echo   Open this URL in any browser (Chrome, Edge, Firefox, or Mobile)
echo  -------------------------------------------------------------------------------
echo.

cd /d "%~dp0"
python src/web_dashboard.py
pause
