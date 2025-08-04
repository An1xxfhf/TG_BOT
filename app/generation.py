from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
dsk = os.getenv("DEEPSEEK_TOKEN")
client = AsyncOpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=dsk,
)

async def gpt_text(text:str):
  completion = await client.chat.completions.create(
   model="deepseek/deepseek-chat",
    messages=[{
      "role":"user",
      "content":text
    }]
  )
  return completion.choices[0].message.content