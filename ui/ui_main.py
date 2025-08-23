import streamlit as st
import requests

from ui_mk import TICKETS_SLIDER # todo html/css templates

API_BASE_URL = "http://localhost:8000"

st.title("EMD Slope Analysis")

st.markdown(TICKETS_SLIDER, unsafe_allow_html=True)

ticket = st.text_input("Ticket:", placeholder="BTCUSDT for example")

if st.button("Get Slope"):
    if ticket:
        with st.spinner(f"Data for {ticket} is loading ..."):
            response = requests.get(f"{API_BASE_URL}/get_slope/{ticket.upper()}")
            result = response.json()
            st.success("**RESULTS**")
            st.write(result)
    else:
        st.warning("Ticket field is empty")
