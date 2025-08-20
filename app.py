from langchain_core.prompts import PromptTemplate
import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_openai.chat_models import ChatOpenAI
st.title("Jambalaya")
dish = st.text_input(label="dish")

openai_key = st.secrets["OPENAI_API_KEY"]

llm = ChatOpenAI()

prompt = PromptTemplate.from_template("Find five recipes for {dish}. Only output links. No titles.")

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

result = chain.invoke({"dish": dish})

st.write(result)
