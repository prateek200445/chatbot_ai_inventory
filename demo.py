from inventory_assistant import InventoryAssistant

def demonstrate_inventory_assistant():
    """
    Demonstrate the InventoryAssistant with sample queries and responses.
    """
    assistant = InventoryAssistant()
    
    sample_queries = [
        "How much should I stock for P001 next week?",
        "What's the forecast for SKU123 for the next 30 days?",
        "Check inventory status for item P002",
        "Do I need to reorder product XYZ tomorrow?"
    ]
    
    print("=== AI Inventory Assistant Demo ===\n")
    
    for i, query in enumerate(sample_queries, 1):
        print(f"Sample Query {i}: {query}")
        response = assistant.handle_query(query)
        print("\nResponse:")
        print(response)
        print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    demonstrate_inventory_assistant()