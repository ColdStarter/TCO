import streamlit as st

# --------------------------
# Page 1: Get Make & Model
# --------------------------
def page_make_model():
    st.title("Enter Car Make and Model")
    
    # Text inputs for make/model
    make = st.text_input("Car Make (e.g., Toyota, Ford, Tesla)", "")
    model = st.text_input("Car Model (e.g., Corolla, F-150, Model 3)", "")
    
    # 'Next' button to proceed
    if st.button("Next"):
        # Store inputs in session state to remember them
        st.session_state["make"] = make
        st.session_state["model"] = model
        # Switch page
        st.session_state["current_page"] = "calculator"

# --------------------------
# Page 2: Calculator
# --------------------------
def page_calculator():
    # Retrieve the make/model from session state
    make = st.session_state.get("make", "Unknown Make")
    model = st.session_state.get("model", "Unknown Model")

    # Show them in the title
    st.title(f"{make} {model} - Lease Calculator")

    # -- Example lease details (you can customize these) --
    purchase_price = st.number_input("Purchase Price", min_value=0.0, value=20000.0)
    lease_months   = st.number_input("Number of Lease Months", min_value=1, value=36)
    
    # Simple monthly cost calculation
    monthly_cost = purchase_price / lease_months
    
    # Display results
    st.write(f"**Monthly Cost**: ${monthly_cost:,.2f}")
    
    # Button to go back to Page 1 if you want
    if st.button("Back"):
        st.session_state["current_page"] = "make_model"

# --------------------------
# Main App Logic
# --------------------------
def main():
    # Initialize session state for current page
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "make_model"  # start on Page 1

    # Route to the correct page
    if st.session_state["current_page"] == "make_model":
        page_make_model()
    else:
        page_calculator()

if __name__ == "__main__":
    main()
