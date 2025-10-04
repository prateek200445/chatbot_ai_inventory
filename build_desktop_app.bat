@echo off
echo Building Inventory Assistant Desktop Application...
echo.

:: Run PyInstaller to create the executable
pyinstaller --name="Inventory Assistant" ^
            --onefile ^
            --windowed ^
            --add-data="inventory_assistant.py;." ^
            inventory_assistant_gui.py

echo.
echo Build complete! The executable is located in the "dist" folder.
echo.
pause