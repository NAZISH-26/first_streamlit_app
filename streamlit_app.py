import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

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



# fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
# streamlit.write('The user entered ', fruit_choice)

# # using API and variabled
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# # Display raw json output 
# # streamlit.text(fruityvice_response.json())


# # normalise json 
# fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# # display normalised json output as table
# streamlit.dataframe(fruityvice_normalized)

# Using try and except for the above code 41 - 50 and creating function
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
# Display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please select fruit to get information')
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()


# Don't run anything past here while we troubleshoot
streamlit.stop()

# # Connecting snowflake
# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# # my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_cur.execute("SELECT * from fruit_load_list")
# # my_data_row = my_cur.fetchone()
# # To get all rows
# my_data_rows = my_cur.fetchall()
# # streamlit.text("Hello from Snowflake:")
# streamlit.header("Fruit load list contains:")
# streamlit.dataframe(my_data_rows)

# Creating function for 73 - 83
streamlit.header("Fruit load list contains:")
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()
  
# Add button to load teh fruit
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)
  
# If this doesn't return 'banana', try changing the select statement to:  

# select * from pc_rivery_db.public.fruit_load_list

add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
