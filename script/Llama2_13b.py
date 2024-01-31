from llama_cpp import Llama

#llm = Llama(model_path="./llama-2-7b-chat.ggmlv3.q8_0.bin")
llm = Llama(model_path="./gguf/llama-2-13b-chat.Q5_K_M.gguf", n_ctx=8192, n_gpu_layers=43);

while True:
    input_text = input('> ')

    output = llm(
        "Q: " + input_text + " A: ",
        max_tokens=0, # increse if you need long answer
        stop=["Q:", "System:", "User:", "Assistant:"], # comment out if you need long answer
        echo=True,
        temperature=0,
    )

    print(output['choices'][0]['text'])
