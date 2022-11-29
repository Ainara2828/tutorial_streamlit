import home
import discoveryPage
import keepVariables
import streamlit as st
from multipage import MultiPage

pages = MultiPage()

pages.add_page("Home",home.run)
pages.add_page("Discovery Page",discoveryPage.run)
pages.add_page("Variable Page",keepVariables.run)


# The main app
pages.run()