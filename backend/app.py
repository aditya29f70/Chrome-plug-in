import os
import re
from flask import Flask, request, jsonify
from langchain_community.document_loaders import WebBaseLoader
from langchain_huggingface import ChatHuggingFace , HuggingFaceEndpoint, HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()



app= Flask(__name__)

@app.route("/ask", methods=["POST"])
def ask():
    data= request.json 
    url= data['url']
    question= data['question']

    llm= HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-1.5B-Instruct", 
    task="text-generation",
    huggingfacehub_api_token= os.getenv("HUGGINGFACEHUB_API_TOKEN") 
    )

    model= ChatHuggingFace(llm= llm)

    embedding= HuggingFaceEmbeddings(model_name= "BAAI/bge-small-en-v1.5")

    parser= StrOutputParser()

## for indexing works 
## first try to do doc loading and then text splitter

    if 'youtube.com' in url or "youtu.be" in url:
        try:
            video_id= url.split('&')[0].split('?')[1].split('=')[1]
            api= YouTubeTranscriptApi()

            transcript_data= api.fetch(video_id, languages=['en'])
            transcript= " ".join(chunk.text for chunk in transcript_data)

            splitter= RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=0
            )

            chunks= splitter.create_documents([transcript])
        except TranscriptsDisabled:
            print("No captions available for this video. ")
        except Exception as e:
            print('error', e)

    else:
        loader= WebBaseLoader(url)

        docs= loader.lazy_load()

        splitter= RecursiveCharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=0
        )

        chunks= splitter.split_documents(docs)

    vector_store= FAISS.from_documents(chunks, embedding)

    ## building Retriever

    retriever= vector_store.as_retriever(search_type="similarity", search_kwargs={"k":2}) 


    ## Augmentation (creating prompt)
    prompt= PromptTemplate(
        template=
        """
        You are a helpful assistant
        Answer ONLY from the provided transcript context.
        If the context is insufficient, just say you don't know.

        {context}
        Question: {question}
        """,
        input_variables=['context', 'question']
    )

    retrieved_docs= retriever.invoke(question)

    def making_context(retrieved_docs):
        context= " ".join(doc.page_content for doc in retrieved_docs)
        return context 
    

    parallel_chain= RunnableParallel({
        'context': retriever | RunnableLambda(making_context),
        'question': RunnablePassthrough()
    })

    # Generation

    chain= parallel_chain | prompt | model | parser

    results= chain.invoke(question)

    return jsonify({"answer": results})





if __name__== "__main__":
    app.run(debug=True)
