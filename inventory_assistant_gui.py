import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
from inventory_assistant import InventoryAssistant

class InventoryAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        self.assistant = InventoryAssistant()
        
        # Configure style
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TButton", background="#007bff", foreground="black", font=("Arial", 10))
        style.configure("TLabel", background="#f0f0f0", font=("Arial", 12))
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="AI Inventory Assistant", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Chat display area
        chat_frame = ttk.Frame(main_frame)
        chat_frame.pack(fill=tk.BOTH, expand=True)
        
        self.chat_display = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, font=("Arial", 11))
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.chat_display.config(state=tk.DISABLED)
        
        # Input area
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, expand=False)
        
        input_label = ttk.Label(input_frame, text="Your Query:")
        input_label.pack(side=tk.LEFT, pady=(0, 10))
        
        self.input_field = ttk.Entry(input_frame, font=("Arial", 11), width=50)
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=(0, 10))
        self.input_field.bind("<Return>", self.process_query)
        
        send_button = ttk.Button(input_frame, text="Send", command=self.process_query)
        send_button.pack(side=tk.RIGHT, pady=(0, 10))
        
        # Sample queries section
        samples_frame = ttk.Frame(main_frame)
        samples_frame.pack(fill=tk.X, expand=False, pady=(10, 0))
        
        samples_label = ttk.Label(samples_frame, text="Sample Queries:", font=("Arial", 10, "bold"))
        samples_label.pack(anchor=tk.W)
        
        sample_queries = [
            "How much should I stock for P001 next week?",
            "What's the forecast for SKU123 for the next 30 days?",
            "Check inventory status for item P002",
            "Do I need to reorder product XYZ tomorrow?"
        ]
        
        for query in sample_queries:
            query_button = ttk.Button(
                samples_frame, 
                text=query,
                command=lambda q=query: self.use_sample_query(q)
            )
            query_button.pack(anchor=tk.W, pady=2, fill=tk.X)
        
        # Initial message
        self.update_chat("👋 Hello! I'm your AI Inventory Assistant.\n"
                         "Ask me about inventory levels, forecasts, or stock recommendations.\n"
                         "You can type your query below or click on one of the sample queries.", "system")
    
    def update_chat(self, message, sender):
        self.chat_display.config(state=tk.NORMAL)
        
        if sender == "user":
            self.chat_display.insert(tk.END, "\n\nYou: ", "user_tag")
            self.chat_display.insert(tk.END, message)
        elif sender == "assistant":
            self.chat_display.insert(tk.END, "\n\nAssistant: ", "assistant_tag")
            self.chat_display.insert(tk.END, message)
        else:
            self.chat_display.insert(tk.END, "\n" + message + "\n")
        
        self.chat_display.tag_configure("user_tag", foreground="#007bff", font=("Arial", 11, "bold"))
        self.chat_display.tag_configure("assistant_tag", foreground="#28a745", font=("Arial", 11, "bold"))
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def process_query(self, event=None):
        query = self.input_field.get().strip()
        if not query:
            return
        
        self.update_chat(query, "user")
        self.input_field.delete(0, tk.END)
        
        # Disable input during processing
        self.input_field.config(state=tk.DISABLED)
        
        # Process query in a separate thread to keep UI responsive
        thread = threading.Thread(target=self.process_query_thread, args=(query,))
        thread.daemon = True
        thread.start()
    
    def process_query_thread(self, query):
        try:
            response = self.assistant.handle_query(query)
        except Exception as e:
            response = f"❌ Error processing your query: {str(e)}"
        
        # Update UI in the main thread
        self.root.after(0, lambda: self.update_chat(response, "assistant"))
        self.root.after(0, lambda: self.input_field.config(state=tk.NORMAL))
    
    def use_sample_query(self, query):
        self.input_field.delete(0, tk.END)
        self.input_field.insert(0, query)
        self.process_query()

def main():
    root = tk.Tk()
    app = InventoryAssistantGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()