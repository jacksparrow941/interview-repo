@echo off
echo ========================================
echo  Interview Repository — Site Builder
echo ========================================
echo.
python generate_site.py
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo  Build successful!
    echo  Starting local server on port 8080...
    echo  Open: http://localhost:8080
    echo  Press Ctrl+C to stop the server.
    echo ========================================
    cd InterviewRepository
    python -m http.server 8080
) else (
    echo.
    echo [ERROR] Build failed. Check the output above.
    pause
)
