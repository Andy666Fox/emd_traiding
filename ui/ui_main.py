import streamlit as st
import requests
import os 

from ui_mk import TICKETS_SLIDER # todo html/css templates
from ui_card import display_card, format_data

API_BASE_URL = os.getenv("API_BASE_URL", "/api")

st.title("EMD Slope Analysis")

st.markdown(TICKETS_SLIDER, unsafe_allow_html=True)

ticket = st.text_input("Ticket:", placeholder="BTCUSDT for example")

if st.button("Get Slope"):
    if ticket:
        with st.spinner(f"Data for {ticket.upper()} is loading ..."):
            response = requests.get(f"{API_BASE_URL}/get_slope_of/{ticket.upper()}")
            result = response.json()
            st.success("**RESULTS**")
            display_card(result)
            st.write(result)
    else:
        st.warning("Ticket field is empty")

with st.sidebar:
    st.info(f"API Parameters")
    if st.button("Check api status"):
        try:
            response = requests.get(f"{API_BASE_URL}/health")
            if response.status_code == 200:
                st.success('Api is healthy')
            else:
                st.error("Api is not responding")
        except:
            st.error('Cannot connect to Api')


