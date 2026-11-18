@echo off
title M-Control AI - Servidor Publico en Vivo (Cloudflare Tunnel)
cd /d "%~dp0"
echo =====================================================================
echo   M-CONTROL AI - INICIANDO SERVIDOR LOCAL Y TUNEL PUBLICO HTTPS
echo =====================================================================
echo.
echo [1/2] Iniciando servidor de IA y Base de Datos en http://127.0.0.1:8088 ...
start "M-Control Server (Puerto 8088)" /min cmd /k "py -m mcontrol_ai.api_service"
timeout /t 3 /nobreak >nul
echo.
echo [2/2] Abriendo enlace publico seguro con Cloudflare Tunnel (HTTP/2)...
echo Copia el enlace que termina en .trycloudflare.com que aparecera abajo:
echo (IMPORTANTE: No cierres esta ventana mientras tus usuarios esten entrando)
echo.
cloudflared.exe tunnel --protocol http2 --url http://127.0.0.1:8088
pause
