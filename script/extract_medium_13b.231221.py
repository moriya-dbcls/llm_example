import sys
import json
from datetime import datetime
from enum import Enum, auto
from typing import List
from pydantic import BaseModel
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.llms import LlamaCpp

class Component(BaseModel):
    name: str
    amount: float
    unit: str

class Medium(BaseModel):
    name: str
    components: List[Component]

class MediumList(BaseModel):
    mediums: List[Medium]

parser = PydanticOutputParser(pydantic_object=MediumList)

model = LlamaCpp(
    model_path="./gguf/llama-2-13b-chat.Q5_K_M.gguf",
    temperature=0,
    n_ctx=8192,
    n_gpu_layers=43,
    #n_gpu_layers=30,
    max_tokens=0,
);

SYS_PROMPT = "You are a curator who investigates the composition of culture media for microorganisms from papers."
FMT_PROMPT = PromptTemplate(
    template="{format_instructions}\n",
    input_variables=["text"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
).format_prompt().to_string()

while True:
    ref_text = input('REFERENCE TEXT: ')
    prompt = "<s>[INST] <<SYS>>\n" + SYS_PROMPT + "\n" + FMT_PROMPT + "\n<</SYS>>\n\nPlease extract culture mediums from the following contexts. If the concentration information is given in terms of \"per liter\", \"/L\", \"%\" etc. in the context, the derived units should reflect this information.\n\n```\n" + ref_text + " \n```\n[/INST] "
    #_input = prompt.format_prompt(text=text)
    #print(prompt)
    #output = model(_input.to_string())
    output = model(prompt)
    print(output)
    #results = parser.parse(output).mediums
    #print(results)

