import streamlit as st

# Set the title of the app
st.title('Quick Streamlit App')

# Input text box
user_input = st.text_input("Enter some text:")

# Display the user input
if user_input:
    st.write("You entered:", user_input)

# Slider for numerical input
number = st.slider("Pick a number", 0, 100)

# Display the selected number
st.write("You picked the number:", number)

# Checkbox
if st.checkbox('Show dataframe'):
    import pandas as pd
    import numpy as np

    df = pd.DataFrame(
        np.random.randn(10, 5),
        columns=('col %d' % i for i in range(5)))

    st.dataframe(df)
