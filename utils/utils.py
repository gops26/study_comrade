import yaml
from langchain_groq import ChatGroq
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain_chroma import Chroma
import os

load_dotenv()


# config
with open("config\\app_config.yml") as f:
    config = yaml.safe_load(f)


def load_config():
    return config


os.makedirs(config["directories"]["persist_directory"], exist_ok=True)


def write_markdown_file(content, filename):
    """
    Writes the given content as a markdown file to the local directory.

    Args:
      content: The String Content to write the file
      filename: the filename to save the file as
    """
    if type(content) == "dict":
        content = "\n".join(f"{key}: {value}" for key,
                            value in content.items())
    if type(content) == list:
        content = "\n".join(content)

    with open(f"{config["directories"]["markdown_output_directory"]}{filename}.md", "w") as f:
        f.write(content)


def load_retriever(pdf_file_path):
    try:
        documents = PyPDFLoader(pdf_file_path).load()
        print("document loaded sucessful ")
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=config["splitter_config"]["chunk_size"], chunk_overlap=config["splitter_config"]["chunk_size"])
        texts = splitter.split_documents(documents)

        bge_embeddings = HuggingFaceBgeEmbeddings(
            model_name=config["embedding_model_config"]["model"],
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        vector_db = Chroma.from_documents(
            documents=texts,
            embeddings=bge_embeddings,
            persist_directory=config["directory"]["persist_directory"]
        )
        print("vector_db saved")
        vector_db.persist()
        return vector_db

    except Exception as e:
        print(e)


def load_llm():
    try:
        llm = ChatGroq(api_key=os.environ["GROQ_API_KEY"],
                       model=config["llm_config"]["model_name"])

        return llm
    except Exception as e:
        print(e)
