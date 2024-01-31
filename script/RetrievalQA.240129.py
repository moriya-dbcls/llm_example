import logging
import sys
import os
import re

# 参考 https://note.com/npaka/n/n3164e8b24539

from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import LlamaCpp
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.document_loaders import PyPDFLoader

if len(sys.argv) < 2:
    print("Usage: RetrievalQA.py [context txt or pdf (e.g. ./langchain/bocchi_en.txt)] (Opt. [model (default:7b, 13b, 70b)] [n_gpu_layers (int)])")
    sys.exit(0)
ms="7b"
ngl=35
if len(sys.argv) >= 3:
    ms=sys.argv[2]
    if ms == "13b":
        ngl=43
    elif ms == "70b":
        ngl=32
if len(sys.argv) >= 4:
    ngl=int(sys.argv[3])

# ログレベルの設定
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, force=True)

# チャンクの確認
#print(len(texts))
#for text in texts:
#    print(text[:10].replace("\n", "\\n"), ":", len(text))

# インデックス
index_dir = "./lc_index/" + sys.argv[1].split('/')[-1].replace('.', '_') + "/"
if os.path.isdir(index_dir):
    # インデックスの読み込み
    index = FAISS.load_local(
        index_dir, HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")
    )
else:
    # ドキュメントの読み込み
    with open(sys.argv[1]) as f:
        txt = re.search('txt$', sys.argv[1])
        pdf = re.search('pdf$', sys.argv[1])
        if txt:
            text_all = f.read()
        elif pdf:
            loader = PyPDFLoader(sys.argv[1])
            text_all = " ".join(str(c.page_content) for c in loader.load_and_split())
        else:
            print(".txt or .pdf")
            sys.exit(0)

    # チャンクの分割
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,  # チャンクの最大文字数
        chunk_overlap=20,  # オーバーラップの最大文字数
    )
    texts = text_splitter.split_text(text_all)

    # チャンクの確認
    #print(len(texts))
    #for text in texts:
    #    print(text[:10].replace("\n", "\\n"), ":", len(text))

    # インデックスの作成 (初回)
    index = FAISS.from_texts(
        texts=texts,
        embedding=HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large"),
    )
    index.save_local(index_dir)

# インデックスの読み込み
#index = FAISS.load_local(
#    "storage", HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")
#)

# LLMの準備
# llm = OpenAI(temperature=0, verbose=True)
llm = LlamaCpp(
    model_path="../gguf/llama-2-" + ms + "-chat.Q5_K_M.gguf",
    n_ctx=8192,
    n_gpu_layers=ngl,
    #main_gpu=0,
    verbose=True,
    temperature=0,
)

# 質問応答チェーンの作成
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=index.as_retriever(search_kwargs={"k": 8}),
    verbose=True,
)

while True:
    input_text = input('> ')
    print("A1:", qa_chain.run(input_text))

# 質問応答チェーンの実行
#print("A1:", qa_chain.run("What kind of person is Hitori Goto?"))
#print("A2:", qa_chain.run("What instrument is Hitori Goto good at?"))
#print("A3:", qa_chain.run("What did Hitori Goto do at the school festival?"))
