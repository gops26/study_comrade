from utils.utils import load_llm, load_retriever, load_config
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import tools_condition, tool_node
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from typing import Annotated
from utils.utils import write_markdown_file, load_config, load_retriever
import shutil
import os

config = load_config()

os.makedirs(config["directories"]["pdf_upload_directory"], exist_ok=True)


config = load_config()


def process_pdf(file):
    # upload pdf
    file_name = os.path.basename(file)
    pdf_file_path = os.path.join(
        config["directories"]["pdf_upload_directory"], file_name)
    print("start retreiver")
    global vector_db

    vector_db = load_retriever(pdf_file_path)
    shutil.copy(file.name, pdf_file_path)
    status = f"file '{file_name}' saved and loaded sucessful"
    print(status)


class State(TypedDict):
    """
    Represents the state of our graph


    """
    messages: Annotated[list, add_messages]
    query: str
    context: str


def retreive_docs(state: State):
    query = state["query"]
    retreiver = vector_db.as_retriever(search_kwargs={"k": 3})
    docs = retreiver.get_relevant_documents(query)
    context = "\n\n".join([doc.page_content for doc in docs])
    state["context"] = context
    return state


def generate_answer(state: State):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Use the context to answer accurately."),
        ("user", "Context: {context}\n\nQuestion: {query}")
    ])
    chain = prompt | load_llm() | StrOutputParser()
    response = chain.invoke(
        {"context": state["context"], "query": state["query"]})
    state["messages"].append(response)
    return state


graph = StateGraph(State)
graph.add_node("retrieve", retreive_docs)
graph.add_node("generate", generate_answer)

graph.add_edge(START, "retrieve")
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)
rag_app = graph.compile()


def gradio_wrapper_func(query, history: list):
    history.append({"role": "user", "content": query})

    result = rag_app.invoke({"messages": [], "query": query, "context": ""})
    history.append(
        {"role": "assistant", "content": result["messages"][-1].content})

    yield result["messages"][-1].content
