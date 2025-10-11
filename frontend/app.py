import streamlit as st
import requests
import time

st.title("Text Echo Bot")

text = st.text_input("Enter text here")

if st.button("Send"):
    if text:
        with st.status("Executing transaction...", expanded=True) as status:
            st.write("Sending request to backend...")
            try:
                response = requests.post("http://backend:8000", json={"text": text})
                if response.status_code == 200:
                    st.write("Received response from backend.")
                    time.sleep(1) # Simulate some processing time
                    status.update(label="Transaction complete!", state="complete", expanded=False)
                    st.write("Backend echoed:")
                    st.write(response.text)
                else:
                    st.error(f"Error from server: {response.status_code}")
                    status.update(label="Transaction failed!", state="error", expanded=False)
            except requests.exceptions.ConnectionError:
                st.error("Error: Could not connect to the server.")
                status.update(label="Transaction failed!", state="error", expanded=False)
