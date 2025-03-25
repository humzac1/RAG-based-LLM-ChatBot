from langchain_core.prompts import PromptTemplate
from langchain import hub
from langchain.schema import StrOutputParser
from langchain.schema.prompt_template import format_document
from langchain.schema.runnable import RunnablePassthrough
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma



def load_text_files(input_dir):
    docs = []
    # Iterate through all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text_content = file.read()
                # Create a Document object for each file
                doc = Document(page_content=text_content, metadata={"source": filename})
                docs.append(doc)
    return docs

def chunk_documents(docs, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, add_start_index=True
    )
    all_splits = text_splitter.split_documents(docs)
    return all_splits


input_directory = 'cleanedText' # Desired input directory

# Load the documents
docs = load_text_files(input_directory)

# Split the documents into chunks
chunked_docs = chunk_documents(docs)

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = ("Your_Gemini_API_Key")

from langchain_google_genai import GoogleGenerativeAIEmbeddings

embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


db = Chroma.from_documents(chunked_docs, embedding_function, persist_directory="vectore_store_gemini")
