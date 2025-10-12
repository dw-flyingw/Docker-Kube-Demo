import streamlit as st
import requests
import time
import os

st.title("Text Echo Bot")

# Initialize session state
if 'echoed_text' not in st.session_state:
    st.session_state.echoed_text = ""

text = st.text_input("Enter text here")

if st.button("Send"):
    if text:
        with st.status("Executing transaction...", expanded=True) as status:
            st.write("Sending request to backend...")
            try:
                response = requests.post(os.getenv("BACKEND_URL", "http://backend:8000"), json={"text": text})
                if response.status_code == 200:
                    st.write("Received response from backend.")
                    time.sleep(1) # Simulate some processing time
                    st.session_state.echoed_text = response.text # Store in session state
                    status.update(label="Transaction complete!", state="complete", expanded=False)
                else:
                    st.error(f"Error from server: {response.status_code}")
                    st.session_state.echoed_text = "" # Clear on error
                    status.update(label="Transaction failed!", state="error", expanded=False)
            except requests.exceptions.ConnectionError:
                st.error("Error: Could not connect to the server.")
                st.session_state.echoed_text = "" # Clear on error
                status.update(label="Transaction failed!", state="error", expanded=False)
    else:
        # Clear the text if the user sends an empty string
        st.session_state.echoed_text = ""


# Display the echoed text if it exists in session state
if st.session_state.echoed_text:
    st.write("Backend echoed:")
    st.markdown(f'<h1 style="color:red;">{st.session_state.echoed_text}</h1>', unsafe_allow_html=True)