import streamlit as st
import datetime
from inventory_assistant import InventoryAssistant

# Initialize the Inventory Assistant
assistant = InventoryAssistant()

# Set page configuration
st.set_page_config(
    page_title="Inventory Assistant",
    layout="wide"
)

# Add header and description
st.title("🤖 AI Inventory Assistant")
st.markdown("""
This assistant helps you manage inventory by providing forecasts, stock levels, and recommendations.
Ask questions about product stock levels, demand forecasts, or when to reorder!
""")

# Add sidebar with sample queries
with st.sidebar:
    st.header("Sample Queries")
    sample_queries = [
        "How much should I stock for P001 next week?",
        "What's the forecast for SKU123 for the next 30 days?",
        "Check inventory status for item P002",
        "Do I need to reorder product XYZ tomorrow?"
    ]
    
    # Create buttons for sample queries
    for query in sample_queries:
        if st.button(query):
            st.session_state.query = query
            st.session_state.run_query = True

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "query" not in st.session_state:
    st.session_state.query = ""
    
if "run_query" not in st.session_state:
    st.session_state.run_query = False

# Display chat history
st.subheader("Conversation")
chat_container = st.container()

with chat_container:
    for entry in st.session_state.chat_history:
        if entry["role"] == "user":
            st.markdown(f"**You**: {entry['content']}")
        else:
            st.markdown(f"**Assistant**: {entry['content']}")
    
    st.divider()

# Create input form
query = st.text_input("Your Query:", value=st.session_state.query)

# Process the query
if st.button("Send") or st.session_state.run_query:
    if query:
        # Add user query to chat history
        st.session_state.chat_history.append({"role": "user", "content": query})
        
        # Get response from assistant
        with st.spinner("Processing your query..."):
            response = assistant.handle_query(query)
        
        # Add assistant response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Reset the query and run_query flag
        st.session_state.query = ""
        st.session_state.run_query = False
        
        # Rerun to update the display
        st.experimental_rerun()

# Add information about the application
st.sidebar.markdown("---")
st.sidebar.subheader("About")
st.sidebar.info("""
This application uses the AI Inventory Assistant to provide inventory forecasts and recommendations.
The assistant connects to the Inventory Forecast API to retrieve data and presents it in a user-friendly format.
""")

# Display the current date
current_date = datetime.datetime.now().strftime("%B %d, %Y")
st.sidebar.markdown(f"**Current Date:** {current_date}")