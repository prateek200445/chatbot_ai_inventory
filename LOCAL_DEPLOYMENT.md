# Local Deployment Guide for Inventory Assistant

This guide explains how to deploy and distribute the Inventory Assistant without using cloud services.

## Option 1: Distribute as a Desktop Application

### Building the Executable

1. **Run the build script**
   - Double-click on `build_desktop_app.bat`
   - Wait for the process to complete
   - Find the executable in the `dist` folder (named "Inventory Assistant.exe")

2. **Distribute the Executable**
   - Copy the executable file to a USB drive
   - Share via file sharing services like Dropbox, Google Drive, or OneDrive
   - Send by email (if file size permits)
   - Host on your own website for download

3. **User Instructions**
   - Users simply need to download and run the executable
   - No installation required
   - Works on Windows systems (for Mac/Linux, you'll need to build on those platforms)

## Option 2: Run as a Local Web Server

You can host the web version on your own computer and allow others on your network to access it.

### Setting Up the Local Server

1. **Start the server**
   - Double-click on `start_local_server.bat`
   - The server will start on port 8501
   - You'll see a URL like `http://0.0.0.0:8501`

2. **Find your computer's IP address**
   - Open Command Prompt and type `ipconfig`
   - Look for the IPv4 Address (e.g., 192.168.1.100)

3. **Sharing access with others**
   - Share the URL with your IP: `http://YOUR_IP_ADDRESS:8501`
   - Others on the same network can access the application via this URL
   - For access outside your network, you'll need to configure port forwarding on your router

## Option 3: Manual Installation

If users are comfortable with Python, they can run the application directly:

1. **Share the code**
   - Zip all files in the project folder
   - Share the zip file

2. **User instructions**
   - Extract the zip file
   - Install Python 3.7 or higher
   - Install dependencies: `pip install -r requirements.txt`
   - Run GUI version: `python inventory_assistant_gui.py`
   - Run web version: `python inventory_assistant_web.py`

## Troubleshooting

### Desktop App Issues
- If antivirus blocks the executable, users may need to add an exception
- Some systems may require additional Visual C++ redistributable packages

### Local Web Server Issues
- Make sure your firewall allows connections on port 8501
- For access issues, try changing the port in the batch file (e.g., to 8080)