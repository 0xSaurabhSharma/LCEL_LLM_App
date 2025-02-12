from fastapi import FastAPI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')

# load llm
llm = ChatGroq(model='Gemma2-9b-it', groq_api_key=groq_api_key)

# prompt template
system_template = 'Translate the following into {lannguage}:'
prompt_template = ChatPromptTemplate.from_messages([
    ('system',system_template),
    ('user','{text}')
])

# parser
parser = StrOutputParser()

## Create chain
chain = prompt_template | llm | parser

## App Defination
app = FastAPI(title='Langchain Server',
              version='1.0',
              description='A simple API server using Langchain runnable interface')

## Adding chain routes
add_routes(
    app,
    chain,
    path='/chain'
)

# entry point and executing the file
if __name__=='__main__':
    import uvicorn
    uvicorn.run(app, 
                host='localhost',
                port=8000)