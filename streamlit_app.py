# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)


cnx = st.connection('snowflake')
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col("fruit_name"))
# st.dataframe(data=my_dataframe, use_container_width=True)

smoothie_name = st.text_input('Name on Smoothie:')

ingredients_list = st.multiselect('Choose up to 5 inredients:', my_dataframe, max_selections=5)

if ingredients_list:

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += f'{fruit_chosen} '


    my_insert_stmt = f""" insert into smoothies.public.orders(ingredients, name_on_order)
            values ('{ingredients_string}', '{smoothie_name}')"""

    st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {smoothie_name}!', icon="✅")
