from dotenv import load_dotenv
import os

from langchain_community.agent_toolkits import SlackToolkit
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_astradb import AstraDBVectorStore
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain.tools.retriever import create_retriever_tool
from langchain import hub

from confluence import fetch_confluence
from github import find_md_files
from note import note_tool
from pdf import fetch_online_pdf_from_file

def connect_to_vstore(collection_name="default"):
    embeddings = OpenAIEmbeddings()
    ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
    ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    desired_namespace = os.getenv("ASTRA_DB_KEYSPACE")

    if desired_namespace:
        ASTRA_DB_KEYSPACE = desired_namespace
    else:
        ASTRA_DB_KEYSPACE = None

    vstore = AstraDBVectorStore(
        embedding=embeddings,
        collection_name=("%s" % collection_name),
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN,
        namespace=ASTRA_DB_KEYSPACE,
    )
    return vstore

def main():
    load_dotenv()

    vstore_mdfiles = connect_to_vstore("github")
    vstore_pdf = connect_to_vstore("pdf")
    vstore_confluence = connect_to_vstore("confluence")

    add_md_files_to_vectorstore = input("Do you want to import the md files? (y/N): ").lower() in ["yes", "y"]

    if add_md_files_to_vectorstore:
        owner = "SDA-SE"
        repo = "sda-dropwizard-commons"
        mdfiles = find_md_files(owner, repo)

        try:
            vstore_mdfiles.delete_collection()
        except Exception as e:
            print(f"Error deleting md files collection: {e}")

        vstore_mdfiles = connect_to_vstore("github")
        vstore_mdfiles.add_documents(mdfiles)

    add_pdf_to_vectorstore = input("Do you want to import the PDF files? (y/N): ").lower() in ["yes", "y"]

    if add_pdf_to_vectorstore:
        alldocs = fetch_online_pdf_from_file("data/pdf_urls.txt")

        try:
            vstore_pdf.delete_collection()
        except Exception as e:
            print(f"Error deleting PDF collection: {e}")

        vstore_pdf = connect_to_vstore("pdf")

        for doc in alldocs:
            vstore_pdf.add_documents(doc)

    add_confluence_pages_to_vectorstore = input("Do you want to import Confluence Pages? (y/N): ").lower() in ["yes", "y"]

    if add_confluence_pages_to_vectorstore:
        confluence_pages = fetch_confluence("solar")

        try:
            vstore_confluence.delete_collection()
        except Exception as e:
            print(f"Error deleting Confluence collection: {e}")

        vstore_confluence = connect_to_vstore("confluence")
        vstore_confluence.add_documents(confluence_pages)

    retriever_md_files = vstore_mdfiles.as_retriever(search_kwargs={"k": 3})
    retriever_tool_md_files = create_retriever_tool(
        retriever_md_files,
        "sda-dropwizard-commons-docs",
        "Use this tool to search our documentation",
    )

    retriever_pdf = vstore_pdf.as_retriever(search_kwargs={"k": 3})
    retriever_tool_pdf = create_retriever_tool(
        retriever_pdf,
        "pdf-retriever",
        "Use this tool to search within PDF files.",
    )

    retriever_confluence = vstore_confluence.as_retriever(search_kwargs={"k": 3})
    retriever_tool_confluence = create_retriever_tool(
        retriever_confluence,
        "confluence-retriever",
        "Use this tool to search Confluence.",
    )

    prompt = hub.pull("hwchase17/openai-functions-agent")
    llm = ChatOpenAI(temperature=0, model="gpt-4o")

    tools = [retriever_tool_md_files, retriever_tool_pdf, retriever_tool_confluence, note_tool]

    slacktoolkit = SlackToolkit()
    slacktools = slacktoolkit.get_tools()
    tools.extend(slacktools)

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    while (question := input("Ask a question about any documentation (q to quit): ")) != "q":
        result = agent_executor.invoke({"input": question})
        print(result["output"])

if __name__ == "__main__":
    main()
