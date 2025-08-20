## Jambalaya

A small app that uses OpenAI, LangChain, and Streamlit to define the “essence” of a recipe. It finds recipes of the same dish, pulls out the ingredients, and find common ingredients across recipes. 

When I cook, I enjoy making my own version of classic dishes. First though, it helps to understand the foundation of the dish which is what inspired this tool.

In the past, I've implemented this idea using other techniques that tend to be far more brittle. Recipe scrapers tend to work only for specific sites, and nowadays recipes are spread across many blogs each with their own formatting. Using NLP to tag parts of ingredients requires more effort to train and calibrate. Here, we can get LLMs to do most of the heavy lifting.