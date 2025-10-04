# Deploying the Inventory Assistant

This guide provides instructions for deploying the Inventory Assistant application for public access using multiple methods.

## Table of Contents
1. [Web Deployment](#web-deployment)
   - [Streamlit Cloud](#streamlit-cloud)
   - [Render](#render)
   - [Heroku](#heroku)
2. [Desktop Application Distribution](#desktop-application-distribution)
   - [Creating an Executable with PyInstaller](#creating-an-executable-with-pyinstaller)
   - [Distribution Methods](#distribution-methods)

## Web Deployment

### Prerequisites
- Install the required dependencies:
  ```
  pip install -r requirements.txt
  ```

### Streamlit Cloud

Streamlit Cloud is the easiest way to deploy the web version of the Inventory Assistant.

1. Create an account on [Streamlit Cloud](https://streamlit.io/cloud)
2. Connect your GitHub account
3. Create a new repository and push your code there
4. From Streamlit Cloud, deploy by selecting:
   - Repository: Your repository
   - Branch: main (or your preferred branch)
   - Main file path: `inventory_assistant_web.py`

The application will be accessible via a URL like: `https://your-app-name.streamlit.app`

### Render

Render is another great platform for deploying Python web apps.

1. Create an account on [Render](https://render.com)
2. Create a new Web Service
3. Connect to your GitHub repository
4. Configure the service:
   - Name: `inventory-assistant`
   - Environment: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run inventory_assistant_web.py --server.port=$PORT --server.address=0.0.0.0`

Render will automatically detect the `Procfile` in your repository.

### Heroku

For Heroku deployment:

1. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Login to Heroku:
   ```
   heroku login
   ```
3. Create a new Heroku app:
   ```
   heroku create inventory-assistant
   ```
4. Push your code to Heroku:
   ```
   git push heroku main
   ```

## Desktop Application Distribution

### Creating an Executable with PyInstaller

To create a standalone executable that users can download and run directly:

1. Install PyInstaller (included in requirements.txt):
   ```
   pip install pyinstaller
   ```

2. Use the provided build script:
   ```
   python build_app.py
   ```

This will create an executable in the `dist` folder.

Alternatively, run PyInstaller directly:

```
pyinstaller --name="Inventory Assistant" --onefile --windowed inventory_assistant_gui.py
```

### Distribution Methods

Once you have the executable file, you can distribute it in several ways:

1. **Host on your website**: Create a download page on your website
2. **GitHub Releases**: Upload the executable as a GitHub release
3. **Cloud Storage**: Upload to services like Google Drive, Dropbox, or OneDrive and share the link
4. **Software Distribution Platforms**:
   - For Windows: Microsoft Store (requires additional packaging)
   - For macOS: Mac App Store (requires additional packaging)
   - For Linux: Package managers like apt, snap, or flatpak

### Considerations

1. **Security**: Desktop apps distributed as executables might trigger antivirus warnings. Consider code signing your application for better trust.
2. **Updates**: Implement an update mechanism or guide users on how to get updates.
3. **Platform Support**: Create separate builds for Windows, macOS, and Linux if you need cross-platform support.