import os
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()

llm= HuggingFaceEndpoint(
repo_id="Qwen/Qwen2.5-1.5B-Instruct", 
task="text-generation",
huggingfacehub_api_token= os.getenv("HUGGINGFACEHUB_API_TOKEN") 
)

model= ChatHuggingFace(llm= llm)

result= model.invoke("who is the prime minister of india?")

print(result.content)