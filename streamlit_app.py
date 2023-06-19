import streamlit
import pandas

streamlit.title ('My parents new healthy diner')

streamlit.header('Breakfast Menu')

streamlit.text('🥣 Omega 3 & Bluberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
# The picker works, but the numbers don't make any sense! We want the customer to be able to choose the fruits by name!!
# so set index to with fruit column
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avacodo','Strawberries'])

# Display the table on the page.
streamlit.dataframe(my_fruit_list)
