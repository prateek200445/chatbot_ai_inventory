@echo off
echo Starting Inventory Assistant Web Server...
echo.

:: Install Streamlit if not already installed
pip install streamlit

:: Run the web application on port 8501 with access from any device on the network
streamlit run inventory_assistant_web.py --server.headless=true --server.port=8501 --server.address=0.0.0.0

echo.
echo Server stopped.
pause