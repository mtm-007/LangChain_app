import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
import streamlit as st
from src.llm_generator.utils import read_file,get_table_data
from src.llm_generator.logger import logging
from src.llm_generator.NLG_Generator import generate_evaluate_chain
#from langchain.callbacks import get_openai_callback
from langchain_community.callbacks import get_openai_callback
from langchain_openai import ChatOpenAI

with open('/Users/mtm007/Downloads/LangChain_app/Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

#title for the streamlit app
st.title(" NLG LangChain Generator APP")

#form UI 
with st.form("user_inputs"):
    #file upload
    upload_file = st.file_uploader("Upload a file or PDF file")

    mcq_count = st.number_input("No. of mcq", min_value=3, max_value=50)
    subject = st.text_input("Insert subject topic", max_chars=20)
    tone = st.text_input("Complexity of questions", max_chars=20, placeholder="simple")

    button= st.form_submit_button("create Questions")

    if button and upload_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text = read_file(upload_file)
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject_topic": subject,
                            "tone": tone,
                            "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )
                #st.write(response)
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")
            
            else:
                print(f"Total tokens: {cb.total_tokens}")
                print(f"Prompt tokens: {cb.prompt_tokens}")
                print(f"completion token: {cb.completion_tokens}")
                print(f"Total cost: {cb.total_cost}")
                if isinstance(response,dict):
                    quiz = response.get("quiz",None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df= pd.DataFrame(table_data)
                            df.index= df.index+1
                            st.table(df)
                            st.text_area(label="Review",value=response["review"])
                        else:
                            st.error("Error in the table data")

                else:
                    st.write(response)


