import streamlit as st
import pandas as pd
import numpy as np

from ui_mk import CARD_STYLE

def format_data(data):
    ticket = data.get('ticket', 'N/A')
    slope = data.get('slope', 0)
    dslope = data.get('dslope', 0)

    color = "🟢" if slope > 0 else "🔴" if slope < 0 else "🟡"
    trend = "📈 Long" if slope > 0 else "📉 Short" if slope < 0 else "➡️ Flat"

    abs_slope = abs(slope)
    if abs_slope < 0.001:
        strength = "Stable"
    elif abs_slope < 0.01:
        strength = "Weak"
    elif abs_slope < 0.05:
        strength = "Initial"
    else:
        strength = "Strong"

    return {
        'ticket': ticket,
        'slope': slope,
        'dslope': dslope,
        'color': color,
        'trend': trend,
        'strength': strength,
    }

def display_card(data):
    formatted = format_data(data)

    with st.container():
        st.markdown(CARD_STYLE.format(formatted['color'], formatted['ticket'], formatted['slope'], 
                                      formatted['dslope'], formatted['trend'], formatted['strength']), unsafe_allow_html=True)