import requests
import json
import datetime
from datetime import date, timedelta
from tabulate import tabulate

class InventoryAssistant:
    """
    AI Inventory Assistant that connects with an Inventory Forecast API
    to provide inventory predictions and recommendations.
    """
    
    def __init__(self):
        self.api_url = "https://model-ai-inventory.onrender.com/forecast"
        self.today = date.today()
    
    def call_api(self, product_id, days=7):
        """
        Call the Inventory Forecast API with parameters.
        
        Args:
            product_id (str): The product ID to get forecast for
            days (int): Number of days to forecast (default: 7)
            
        Returns:
            dict: JSON response from the API
        """
        payload = {
            "product_id": product_id,
            "days": days
        }
        
        try:
            # Try to use API with timeout to prevent long hanging connections
            response = requests.post(self.api_url, json=payload, timeout=5)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API connection error: {str(e)}")
            # If API is unreachable, use mock data for demonstration
            return self.get_mock_data(product_id, days)
            
    def get_mock_data(self, product_id, days=7):
        """
        Generate mock data for demonstration when API is unreachable.
        
        Args:
            product_id (str): The product ID for the mock data
            days (int): Number of days to generate mock forecast
            
        Returns:
            dict: Mock API response
        """
        import random
        from datetime import date, timedelta
        
        # Generate realistic-looking mock data
        today = date.today()
        reorder_point = random.randint(450, 550)
        safety_stock = random.randint(2, 10)
        current_stock = random.randint(reorder_point - 50, reorder_point + 100)
        
        # Generate forecast data
        forecast = {}
        base_demand = random.randint(80, 120)
        
        for i in range(days):
            forecast_date = (today + timedelta(days=i)).strftime("%Y-%m-%d")
            daily_forecast = base_demand + random.randint(-20, 20)
            lower_bound = int(daily_forecast * 0.8)
            upper_bound = int(daily_forecast * 1.2)
            
            forecast[forecast_date] = {
                "forecast": daily_forecast,
                "lower_bound": lower_bound,
                "upper_bound": upper_bound
            }
        
        # Generate warnings based on stock levels
        warnings = []
        days_to_reorder = (current_stock - safety_stock) / base_demand
        if days_to_reorder < days:
            warnings.append(f"Stock will reach reorder point in approximately {int(days_to_reorder)} days")
        if current_stock < reorder_point:
            warnings.append("Current stock is below reorder point")
        
        # Create mock response
        mock_response = {
            "Reorder Point": reorder_point,
            "Safety Stock": safety_stock,
            "Current Stock": current_stock,
            "Forecast": forecast,
            "Warnings": warnings
        }
        
        # Add a note that this is mock data
        mock_response["Note"] = "Using mock data for demonstration (API unreachable)"
        
        return mock_response
    
    def format_date(self, date_str):
        """Format date string to a more readable format"""
        try:
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return date_obj.strftime("%d %b, %Y")
        except:
            return date_str
    
    def process_response(self, response):
        """
        Process API response into a user-friendly format.
        
        Args:
            response (dict): API response in JSON format
            
        Returns:
            str: Formatted user-friendly response
        """
        if "error" in response:
            return f"❌ {response['error']}"
        
        # Extract key information
        reorder_point = response.get("Reorder Point")
        safety_stock = response.get("Safety Stock")
        current_stock = response.get("Current Stock", "Unknown")
        forecast_data = response.get("Forecast", {})
        plot_url = response.get("Plot URL", None)
        warnings = response.get("Warnings", [])
        mock_note = response.get("Note", None)
        
        # Create a summary response
        output = []
        
        # Main insight
        if current_stock != "Unknown" and reorder_point is not None:
            if current_stock <= reorder_point:
                output.append(f"📉 **Stock Alert: Current stock ({current_stock} units) is at or below reorder point!**")
            else:
                output.append(f"📊 **Stock Status: Current stock ({current_stock} units) is above reorder point.**")
        else:
            output.append("📊 **Inventory Forecast Summary:**")
        
        # Key numbers
        output.append("\n**Key Inventory Numbers:**")
        if reorder_point is not None:
            output.append(f"➡️ Reorder Point: **{reorder_point} units** (place order when stock drops to this level)")
        if safety_stock is not None:
            output.append(f"➡️ Safety Stock: **{safety_stock} units** (minimum buffer to maintain)")
        if current_stock != "Unknown":
            output.append(f"➡️ Current Stock: **{current_stock} units**")
        
        # Forecast data
        if forecast_data:
            output.append("\n**Demand Forecast:**")
            forecast_table = []
            headers = ["Date", "Forecast", "Range"]
            
            # Sort dates chronologically
            sorted_dates = sorted(forecast_data.keys())
            
            for date_str in sorted_dates:
                forecast_info = forecast_data[date_str]
                forecast_val = forecast_info.get("forecast", "N/A")
                lower_bound = forecast_info.get("lower_bound", "N/A")
                upper_bound = forecast_info.get("upper_bound", "N/A")
                
                forecast_val = round(forecast_val, 1) if isinstance(forecast_val, (int, float)) else forecast_val
                lower_bound = round(lower_bound, 1) if isinstance(lower_bound, (int, float)) else lower_bound
                upper_bound = round(upper_bound, 1) if isinstance(upper_bound, (int, float)) else upper_bound
                
                range_val = f"{lower_bound}–{upper_bound}" if lower_bound != "N/A" and upper_bound != "N/A" else "N/A"
                formatted_date = self.format_date(date_str)
                
                forecast_table.append([formatted_date, forecast_val, range_val])
            
            output.append(tabulate(forecast_table, headers=headers, tablefmt="pipe"))
        
        # Priority alerts/warnings
        if warnings:
            output.append("\n⚠️ **Priority Alerts:**")
            for warning in warnings:
                output.append(f"- {warning}")
        
        # Actionable advice
        output.append("\n**Recommendations:**")
        if current_stock != "Unknown" and reorder_point is not None:
            if current_stock <= reorder_point:
                output.append("🚨 **Place an order immediately** to avoid stockouts.")
            elif current_stock <= reorder_point * 1.2:
                output.append("⚠️ **Consider placing an order soon** as stock is getting close to reorder point.")
            else:
                output.append("✅ Stock levels look good. No immediate action required.")
        else:
            if reorder_point is not None:
                output.append(f"📝 Monitor stock levels and place orders when they drop below {reorder_point} units.")
        
        # If forecast chart is available
        if plot_url:
            output.append(f"\n📈 A forecast chart is available at: {plot_url}")
            
        # Add mock data note if present
        if mock_note:
            output.append(f"\n🔍 Note: {mock_note}")
        
        return "\n".join(output)
    
    def handle_query(self, query):
        """
        Process user query and return appropriate response.
        
        Args:
            query (str): User query about inventory
            
        Returns:
            str: Formatted response to user query
        """
        # Extract product_id and days from query
        product_id = None
        days = 7  # Default days
        
        import re
        
        # Look for product_id=X pattern first (most explicit)
        product_match = re.search(r'product_id[=\s:]+([a-zA-Z0-9]+)', query)
        if product_match:
            product_id = product_match.group(1).upper()
        
        # If not found, try a more comprehensive pattern that can find product IDs in natural language
        if not product_id:
            # Match product IDs that follow patterns like P001, SKU123, etc. in natural language
            # This will find product IDs that are:
            # 1. Preceded by "for", "product", "item", "sku", etc.
            # 2. Standalone with a letter followed by numbers (P001, A123, etc.)
            patterns = [
                # Product followed by ID - e.g., "product P001", "for P001", "of P001"
                r'(?:for|product|item|sku|of|on|about)\s+([A-Za-z][A-Za-z0-9]{2,})',
                # IDs with prefixes - e.g., "P-001", "SKU-123"
                r'(?:[A-Za-z]+[-:]([0-9]{3,}))',
                # Standard product IDs - e.g., "P001", "SKU123"
                r'\b([A-Za-z][0-9]{3,})\b',
                # Any alphanumeric string that looks like a product ID
                r'\b([A-Za-z][A-Za-z0-9]{2,})\b'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, query)
                if matches:
                    # Take the first match
                    product_id = matches[0].upper()
                    break
                
        # If still not found, check if query itself is just a product ID (e.g., "P001")
        if not product_id and re.match(r'^[a-zA-Z0-9]+$', query.strip()):
            product_id = query.strip().upper()
        
        # Look for time periods
        time_patterns = {
            'day': 1,
            'tomorrow': 1,
            'week': 7,
            'month': 30,
            'quarter': 90
        }
        
        for pattern, days_value in time_patterns.items():
            if pattern in query.lower():
                days = days_value
                break
        
        # Check for specific number of days
        days_match = re.search(r'(\d+)[\s-]*(day|days)', query.lower())
        if days_match:
            days = int(days_match.group(1))
        
        # If no product ID found, ask for it
        if not product_id:
            return "I need a product ID to check inventory forecast. Please specify a product ID (e.g., P001)."
        
        # Call API and format response
        response = self.call_api(product_id, days)
        return self.process_response(response)


# Main function to handle user interaction
def main():
    assistant = InventoryAssistant()
    print("👋 Hello! I'm your AI Inventory Assistant.")
    print("Ask me about inventory levels, forecasts, or stock recommendations.")
    print("Type 'exit' or 'quit' to end the conversation.\n")
    
    while True:
        user_input = input("Your query: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye! Have a great day.")
            break
        
        response = assistant.handle_query(user_input)
        print("\n" + response + "\n")


if __name__ == "__main__":
    main()