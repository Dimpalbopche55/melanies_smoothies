import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Input for the name on the order
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Establish Snowflake connection
  with st.connection('snowflake') as cnx:
    session = cnx.session()
    my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).to_pandas()
    
    # Create a multiselect for ingredients
    ingredients_list = st.multiselect(
        'Choose up to 5 ingredients:',
        my_dataframe['FRUIT_NAME'].tolist(),
        max_selections=5
    )

    if ingredients_list:
        ingredients_string = ', '.join(ingredients_list)

        my_insert_stmt = f"""
            INSERT INTO smoothies.public.orders (ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """

        st.write(my_insert_stmt)

        # Button to submit order
        time_to_insert = st.button('Submit Order')

        if time_to_insert:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!')
