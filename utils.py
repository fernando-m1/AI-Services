from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ChatMessageHistory
from langchain.chat_models import ChatOpenAI
from langchain.chains.base import Chain
from langchain.chains import LLMChain
from langchain.callbacks import get_openai_callback

#import magic
import os
import nltk
import config
import inspect
import tiktoken
from getpass import getpass
from typing import Any
from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

# ##### **Language Model**
# Inicializar modelo de lenguaje.
llmChatGPT = ChatOpenAI(
    temperature=0.5,
    openai_api_key=os.environ['OPENAI_API_KEY'],
    model="gpt-4-32k",
    streaming=False
)

# ##### **Prompt Template**
# Prompt Template para reformatear dirección:

template = """
Te voy a dar una dirección, y necesito que me ayudas a cambiar el formato de la dirección siguiendo las siguientes reglas:

- Todos los números que recibas deben ser regresados en número y texto de forma consecutiva (por ejemplo, si el número exterior es "1500", conviértelo a "1500, mil quinientos"); no te olvides de también agregar el número, no solo el texto.
- No pueden existir abreviaciones (por ejemplo, convertir "C.P." a "código postal").
- El orden del domicilio debe ser nombre de calle o vialidad; número exterior; número interior (si lo hay); colonia, fraccionamiento o condominio; código postal; municipio; estado; país. Si falta alguno de estos datos en el domicilio que tú conozcas, agrégalo.
- El número del código postal siempre lo describes en texto deletréandolo.
- Si te encuentras un guión (-), lo vas a escribir explícitamente como "guión".
- No respondas nada más que el domicilio.
- "#100-38" se convierte en "número 100-38, cien, guión, treinta y ocho"
- "350-A" se convierte en "350-A, trescientos cincuenta, guión, letra A"
- "coto" es un condominio, pero no lo renombraremos, se mantendrá como "Coto"
- Ejemplo: "Blvd. Bosques de Santa Anita 2355, Local 4, Santa Anita, C.P. 45645, Tlajomulco de Zuñiga, Jalisco" debe ser formateado a "Boulevard Bosques de Santa Anita número 2355 dos mil quinientos cincuenta y cinco, Local 4 cuatro, Colonia Santa Anita, Código Postal 45645, cuatro, cinco, seis, cuatro, cinco, Tlajomulco de Zúñiga, Jalisco, México.

Dirección original: {input_address}
Dirección formateada: """

prompt_template = PromptTemplate(
    input_variables=["input_address"],
    template=template
)

# ##### **Prompt**
def create_chain() -> Any:
    llm_chain = LLMChain(
        llm=llmChatGPT,
        prompt=prompt_template,
        verbose=False,
        )
    
    return llm_chain