import streamlit as st
import numpy as np
import pandas as pd
import time
from persist import persist, load_widget_state

def run():

    #put that in order to save variables between pages
    load_widget_state()

    # Create title
    st.title('Example App with Streamlit')

    st.header("Widget and session state")

    # widget and session state

    #initialise key of the element in session state
    if "name" not in st.session_state:
        st.session_state.name =""

    #create your function
    def saveVar():
        st.write("Your name is : ")
        st.write(st.session_state.name)

    #text enter area to be saved
    st.text_input("Your name", key="name", on_change=saveVar)

    st.header("Dataframe")

    # Create dataframe
    dataframe = pd.DataFrame(
        np.random.randn(10, 20),
        columns=('col %d' % i for i in range(20)))


    #df with max values highlighted
    st.dataframe(dataframe.style.highlight_max(axis=0))

    st.header("Other objects")

    #slide bar from 1 to 100
    x = st.slider('x', key = persist("slide_x_squared"))  # 👈 we put persist here to send the key to other pages
    st.write(x, 'squared is', x * x)



    #choose beyond dropdown list
    option = st.selectbox(
        'Which variable / column from df do you want to select?',
        dataframe.columns)

    'You selected: ', option


    # display object on the right side : sidebar
    add_selectbox = st.sidebar.selectbox(
        'How would you like to be contacted?',
        ('Email', 'Home phone', 'Mobile phone')
    )



    # create columns and nice display
    left_column, right_column = st.columns(2)
    # You can use a column just like st.sidebar:
    left_column.button('Column 1')
    with right_column:
        st.button('Column 2')

        #radio selection widget
        chosen = st.radio(
            'Sorting hat',
            ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
        st.write(f"You are in {chosen} house!")

    #introduce image
    st.image("https://static.streamlit.io/examples/cat.jpg")

    #add progress bar
    'Starting a long computation...'

    # Add a placeholder
    latest_iteration = st.empty() #Inserts a container into your app that can be used to hold a single element. This allows you to, for example, remove elements at any point, or replace several elements at once
    bar = st.progress(100)

    for i in range(100):
    # Update the progress bar with each iteration.
        latest_iteration.text(f'Iteration {i+1}')
        bar.progress(i + 1)
        time.sleep(0.01)

    '...and now we\'re done!'

    st.header("Load data")


    DATE_COLUMN = 'date/time'
    DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

    st.header("use cache")

    @st.cache
    def load_data(nrows):
        data = pd.read_csv(DATA_URL, nrows=nrows)
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
        return data


    # Create a text element and let the reader know the data is loading.
    data_load_state = st.text('Loading data...')
    # Load 10,000 rows of data into the dataframe.
    data = load_data(10000)
    # Notify the reader that the data was successfully loaded.
    data_load_state.text('Loading data...done (using cache)!')

    # display data
    st.subheader('Raw data')
    st.write(data)


    st.header("some graphs")

    #plot hist and map
    st.subheader('Number of pickups by hour')

    hist_values = np.histogram(
        data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
    st.bar_chart(hist_values)

    st.header("Communication between two widgets")

    st.subheader('Map of pickups at selected time')
    hour_to_filter = st.slider('hour', 0, 23, 17)
    filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
    st.subheader(f'Map of all pickups at {hour_to_filter}:00')
    st.map(filtered_data)


    #checkbox to display data
    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)

