from langchain import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import WebBaseLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

from dotenv import load_dotenv
load_dotenv()

loader = WebBaseLoader("https://freemocap.readthedocs.io/en/latest/")
docs = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
ruff_texts = text_splitter.split_documents(docs)
embeddings = OpenAIEmbeddings()
freemocap_docs_db = Chroma.from_documents(ruff_texts, embeddings, collection_name="freemocap_docs")
llm = OpenAI(temperature=0)
freemocap_retrieval_qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=freemocap_docs_db.as_retriever())

