from collections import Counter
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_openai.chat_models import ChatOpenAI
import re

openai_key = st.secrets["OPENAI_API_KEY"]

st.title("Find the essence of a dish")

llm = ChatOpenAI()

dish = st.text_input(label="dish")
submit = st.button("Find recipes")

find_recipes_prompt = PromptTemplate.from_template("Find five recipes for {dish}. Only output links. No titles.")

get_ingredients_prompt = PromptTemplate.from_template("Visit this web site {recipe} and list ingredient strings without quantity, units, or descriptors. List one ingredient per line and leave off numbers, bullet points, dashes, and anything that prefixes ingredients in the list.")

output_parser = StrOutputParser()

find_recipes_chain = find_recipes_prompt | llm | output_parser

get_ingredients_chain = get_ingredients_prompt | llm | output_parser 

full_chain = RunnablePassthrough.assign(recipe=find_recipes_chain).assign(ingredients=get_ingredients_chain)
ingredient_tally = Counter()
if submit and dish:
    result = full_chain.invoke({"dish": dish})
    recipes = find_recipes_chain.invoke({"dish": dish})
    recipes = [r.strip() for r in recipes.splitlines() if r.strip()]
    ingredients_lists = get_ingredients_chain.map().invoke(recipes)
    cleaned_ingredients = []
    for ingredient_list in ingredients_lists:
        cleaned_ingredients = []
        ingredients = ingredient_list.splitlines()
        for ingredient in ingredients:
            ingredient = re.sub(r'^\d+[\.\)\-]?\s*', '', ingredient)
            ingredient = ingredient.replace(',', '').replace('-', '')
            ingredient = ingredient.lower().strip()
            cleaned_ingredients.append(ingredient)   
        ingredient_tally.update(cleaned_ingredients) 
    sorted_ingredients = [ingredient for ingredient,_ in sorted(ingredient_tally.items(), key=lambda x: (-x[1], x[0]))]
    st.write(', '.join([ingredient.title() for ingredient in sorted_ingredients]))
