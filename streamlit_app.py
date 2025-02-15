# Import python packages
import streamlit as st
import requests as rq
import pandas as pd
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

cnx = st.connection('snowflake')
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col("fruit_name"), col("search_on"))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

pd_df = my_dataframe.to_pandas()

smoothie_name = st.text_input('Name on Smoothie:')

ingredients_list = st.multiselect('Choose up to 5 inredients:', my_dataframe, max_selections=5)

if ingredients_list:

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += f'{fruit_chosen} '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]

        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(f'{fruit_chosen} Nutrition Information')
        
        sf_res = rq.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        sf_df = st.dataframe(sf_res.json(), use_container_width=True)


    my_insert_stmt = f""" insert into smoothies.public.orders(ingredients, name_on_order)
            values ('{ingredients_string}', '{smoothie_name}')"""

    st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {smoothie_name}!', icon="✅")