from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import re
from langchain import PromptTemplate
from tqdm import tqdm
import torch
import time
from datetime import datetime
import numpy as np
# Initialize the DeepSeek model
model_id = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto", trust_remote_code=True)
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512,
    output_hidden_states = True,
    output_attention = True,
    temperature=0.6,  # Recommended by DeepSeekModel
    top_p=0.95,       # Recommended by DeepSeekModel
    trust_remote_code=True
)

# Initialize LangChain pipeline
llm = HuggingFacePipeline(pipeline=pipe)