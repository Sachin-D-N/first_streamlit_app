import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError

#streamlit.title("My Mom's New Healthy Diner")

streamlit.header('Breakfast Favorites')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#adding steps for API
#import requests
streamlit.header("Fruityvice Fruit Advice!")

#user chice
def get_fruity_wise_data(fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice )
  #streamlit.text(fruityvice_response.json())
  #write your own comment -normalize the output
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
try :
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('please select a fruit to get information')
  else:
    #streamlit.write('The user entered ', fruit_choice)
    back_from_function=get_fruity_wise_data(fruit_choice)
      
    # write your own comment - converts in to dataframe
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()






streamlit.header("View Our Fruit List - Add Your Favorites !")
#snow flake related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()

#add a button to load a fruit
if streamlit.button('Get Fruit List '):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)

#allow the end user to add the fruit into the list

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
    return "Thanks for Adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?' )
if streamlit.button('Add fruits into the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_fucntion=insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_fucntion)
  

  
  

streamlit.stop()
  
  
    

#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("select * from fruit_load_list")
#my_data_row = my_cur.fetchone()
my_data_row = my_cur.fetchall()
#streamlit.header("The fruit load list contains :")
#streamlit.dataframe(my_data_row)

add_fruit = streamlit.text_input('What fruit would you like add?','jackfruit')
streamlit.write('The user entered ', add_fruit)
streamlit.write('Thanks for adding ', add_fruit)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")




