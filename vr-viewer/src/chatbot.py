# File: chatbot.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate

# Initialize FastAPI app
app = FastAPI()

# CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend origin for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input schema
class Query(BaseModel):
    question: str

# Load model and tokenizer
model_id = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto", trust_remote_code=True)

# Create pipeline
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512,
    temperature=0.6,
    top_p=0.95,
    trust_remote_code=True
)

# Wrap in LangChain
llm = HuggingFacePipeline(pipeline=pipe)

# Prompt template
cot_prompt = PromptTemplate(
    input_variables=["question"],
    template="Answer the following question step by step concisely and at the end, provide the final numeric answer as a single number (integer or decimal) on a new line: {question}"
)

@app.post("/chat")
async def chat(query: Query):
    prompt = cot_prompt.format(question=query.question)
    response = llm(prompt)
    return {"response": response}
