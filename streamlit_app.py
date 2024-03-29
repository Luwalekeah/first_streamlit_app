import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')


streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)


# New section to display fruityvice api response
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  # Take the json version of the response and normalize it
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
# New section to display fruityvice api response  
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get informaiton.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
# dont run anything past here while we troubleshoot
except URLError as e:
  streamlit.error()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)

# streamlit.header("View Our Fruit List - Add your Favorites!")
# # Snowflake related functions
# def get_fruit_load_list():
#   with my_cnx.cursor() as my_cur:
#     my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
#     return my_cur.fetchall()

# # Add a button to load the fruit
# if streamlit.button('Get Fruit Load List'):
#   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#   my_data_rows = get_fruit_load_list()
#   my_cnx.close()
#   streamlit.dataframe(my_data_rows)


# I am commenting this code out because i dont ahve access to a snowflake db, maybe i can use Azure?

# Allow the end user to add a fruit to the list
# def insert_row_snowflake(new_fruit):
#   with my_cnx.cursor() as my_cur:
#     my_cur.execute("INSERT INTO FRUIT_LOAD_LIST VALUES ('" + new_fruit +"')")
#     return "Thanks for adding " + new_fruit

# add_my_fruit = streamlit.text_input('What fruit would you like to add?','')
# if streamlit.button('Add a Fruit to the list'):
#   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#   back_from_function = insert_row_snowflake(add_my_fruit)
#   streamlit.text(back_from_function)
