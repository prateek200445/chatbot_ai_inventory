# Define Python build spec for packaging desktop application with PyInstaller

import PyInstaller.__main__
import os
import sys

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Application name and entry point
app_name = "Inventory Assistant"
script_path = os.path.join(script_dir, "inventory_assistant_gui.py")

# Run PyInstaller
PyInstaller.__main__.run([
    script_path,
    "--name=%s" % app_name,
    "--onefile",
    "--windowed",
    "--add-data=%s:." % os.path.join(script_dir, "inventory_assistant.py"),
    "--icon=%s" % os.path.join(script_dir, "icon.ico") if os.path.exists(os.path.join(script_dir, "icon.ico")) else ""
])

print(f"Application {app_name} packaged successfully!")