from persist import persist, load_widget_state
import streamlit as st
import pandas as pd

def run():

    load_widget_state()

    st.write("In the previous page, you have sent with the function persist the slide object with the key value slide_x_squared")
    st.write("We can then print that value here, each time it's updated, the value will be saved and udpated here too")
    st.write(st.session_state.slide_x_squared)