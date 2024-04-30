import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate

import sys
import json
import re
import os
from datetime import datetime
from enum import Enum, auto
from langchain.output_parsers import PydanticOutputParser

model_id = "NousResearch/Meta-Llama-3-8B-Instruct"
peft_name = "./tmp_script/fine-tune/cellosaurus_peft/llama3-8b-ft/checkpoint-4000"

tokenizer = AutoTokenizer.from_pretrained(model_id)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    torch_dtype="auto"
)
model.resize_token_embeddings(128257)

model = PeftModel.from_pretrained(
    model,
    peft_name,
    device_map="auto"
)

with open(sys.argv[1]) as file:
    for d in json.load(file):
        is_file = os.path.isfile('./langchain/out_cellosaurus/' + d['accession'] + '.txt')
        if is_file:
            continue
        ref_text = ''
        for k in d.keys():
            ref_text += " " + k + " is '" + d[k] + "'."
        if len(ref_text) > 10000:
            continue
        messages = [{"role": "use", "content": "You are a biological ontologist. Please extract the name of the cell line from the following text and return it in JSON format. Then, the JSON schema is follows:\n```{\"properties\": {\"cell_line_name\":{\"title\":\"Cell_line_name\", \"type\":\"string\"}}}```.\nNote typos and misunderstandings in the given text.\n```" + ref_text + "```." }]
        inputs = tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(model.device)
        with torch.no_grad():
            outputs = model.generate(
                inputs,
                max_new_tokens=100,
                do_sample=True,
                temperature=0.0001,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )
            with open('./langchain/out_cellosaurus/' + d['accession'] + '.txt', 'w') as f:
                f.write(re.sub(r'.assistant[\s\S]*', '.', re.sub(r'[\s\S]+```.assistant', '', tokenizer.decode(outputs[0], skip_special_tokens=True))))






