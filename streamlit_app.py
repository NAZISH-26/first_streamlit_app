import streamlit
import pandas
import requests
import snowflake.connector

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

# make the table below the picker a bit smarter so it's doesn't load all the fruits, just the ones shown in the pick list. 
# We'll ask our app to put the list of selected fruits into a variable called fruits_selected.
# Then, we'll ask our app to use the fruits in our fruits_selected list to pull rows from the full data set (and assign that data to a variable called fruits_to_show)

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# Display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

# using API and variabled
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# Display raw json output 
# streamlit.text(fruityvice_response.json())


# normalise json 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# display normalised json output as table
streamlit.dataframe(fruityvice_normalized)


# Connecting snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchone()
# streamlit.text("Hello from Snowflake:")
streamlit.text("Fruit load list contains:")
streamlit.text(my_data_row)
