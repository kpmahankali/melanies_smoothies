# Import python packages
import streamlit as st
import snowflake.connector
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!""")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Snowflake connection parameters
snowflake_params = {
    "account" == "QSXNGXH.XKB93585",
    "user" == "kpmahankali2",
    "password" == "Bilva@3189",
    "role" == "SYSADMIN",
    "warehouse" == "COMPUTE_WH",
    "database" == "SMOOTHIES",
    "schema" == "PUBLIC"
}

conn = snowflake.connector.connect(snowflake_params)
# conn = snowflake.connector.connect('snowflake')
session = conn.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Choose upto 5 ingredients:', my_dataframe)

if ingredients_list:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(('Your Smoothie is ordered,' + name_on_order + '!'), icon="✅")
