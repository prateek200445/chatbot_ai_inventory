# AI Inventory Assistant

An AI assistant that connects with an Inventory Forecast API to provide inventory predictions and recommendations in a user-friendly format.

![Inventory Assistant Banner](https://via.placeholder.com/800x200?text=Inventory+Assistant)

## Features

- Connects to the Inventory Forecast API at `https://model-ai-inventory.onrender.com/forecast`
- Takes user queries about inventory, stock, or forecast
- Calls the API with appropriate parameters (product ID, days, etc.)
- Interprets API responses into clear, human-friendly terms
- Provides structured explanations with:
  - Short summaries of main insights
  - Key numbers in bullets and tables
  - Actionable advice
  - Priority alerts and warnings

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:

```
pip install -r requirements.txt
```

## Usage

### Command Line Interface

Run the script:

```
python inventory_assistant.py
```

### Graphical User Interface

For a more user-friendly experience, you can use the GUI version:

```
python inventory_assistant_gui.py
```

The GUI includes sample queries you can click on and a chat-like interface for interacting with the assistant.

### Example Queries

Enter queries about inventory like:

- "How much should I stock for P001 next week?"
- "What's the forecast for SKU123 for the next 30 days?"
- "Check inventory status for item P002"
- "Do I need to reorder product XYZ tomorrow?"

The assistant will extract the product ID and time period from your query, call the API, and present the results in a user-friendly format.

## API Response Format

The API returns JSON data with the following structure:

```json
{
  "Reorder Point": 498,
  "Safety Stock": 3,
  "Current Stock": 500,
  "Forecast": {
    "2023-10-04": {
      "forecast": 99.96,
      "lower_bound": 77.2,
      "upper_bound": 124.04
    },
    "2023-10-05": {
      "forecast": 95.5,
      "lower_bound": 75.1,
      "upper_bound": 120.8
    },
    ...
  },
  "Warnings": [
    "Stock level will reach reorder point in 3 days",
    "High demand variability detected"
  ],
  "Plot URL": "https://example.com/forecast-plot.png"
}
```

The assistant converts this information into easily understood text with appropriate formatting.

## Requirements

- Python 3.7+
- requests
- tabulate
- streamlit (for web version)
- pyinstaller (for packaging desktop app)

## Deployment

This application can be deployed in multiple ways:

### Web Application

The Inventory Assistant includes a web version using Streamlit. To run it locally:

```bash
pip install streamlit
streamlit run inventory_assistant_web.py
```

For deploying to cloud platforms like Streamlit Cloud, Render, or Heroku, see [DEPLOYMENT.md](DEPLOYMENT.md).

### Desktop Application

You can package the desktop GUI version into a standalone executable:

```bash
python build_app.py
```

This will create an executable in the `dist` folder that can be distributed to users.

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).