import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title('My parents new Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 and bluberry oatmeal')
streamlit.text('🥬Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avacado Toast')
streamlit.header('🍉🍇Build Your Own Fruit Smoothie🥤🍐')
my_fruit_list=pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# Let's put a pick list here so they can pick the fruit they want to include 
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
#display the table on the page
streamlit.dataframe(fruits_to_show)
#create the repeatable code block(function)
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +fruit_choice)
  #streamlit.text(fruityvice_response.json()) # just writes the data to the screen.
  #take the json version of response and normalize it.
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  # O/P it the screen as a table.
  return fruityvice_normalized
streamlit.header("Fruityvice Fruit Advice!")#New section to display fruityvice API response.
try:
  fruit_choice=streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("please select fruit to get information")
  else:
    back_from_function=get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()
streamlit.header("This fruit load list contains:")
#Snowflake related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()
#add a button to load the list
if streamlit.button('Get fruit load list:'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      my_data_rows=get_fruit_load_list()
      streamlit.dataframe(my_data_rows)
      #dont run anything past here while troubleshoot.
#Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
      with my_cnx.cursor() as my_cur:
         my_cur.execute("insert into fruit_load_list values('from streamlit')")
         return "Thanks for adding "+new_fruit
add_my_fruit=streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Get fruit load list:'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      back_from_function=insert_row_snowflake(add_my_fruit)
      streamlit.text(back_from_function)
streamlit.text("Thanks for adding Jackfruit")
