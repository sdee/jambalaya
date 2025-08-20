from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_openai.chat_models import ChatOpenAI

openai_key = st.secrets["OPENAI_API_KEY"]

st.title("Jambalaya")

llm = ChatOpenAI()

dish = st.text_input(label="dish")
submit = st.button("Find recipes")

find_recipes_prompt = PromptTemplate.from_template("Find one recipes for {dish}. Only output links. No titles.")

get_ingredients_prompt = PromptTemplate.from_template("Visit this web site {recipe} and list ingredient strings without quantity, units, or descriptors.")

output_parser = StrOutputParser()

find_recipes_chain = find_recipes_prompt | llm | output_parser

get_ingredients_chain = get_ingredients_prompt | llm | output_parser 

full_chain = RunnablePassthrough.assign(recipe=find_recipes_chain).assign(ingredients=get_ingredients_chain)
if submit and dish:
    result = full_chain.invoke({"dish": dish})
    st.write(result['ingredients'])
