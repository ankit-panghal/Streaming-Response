from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
import os, json

load_dotenv()

app = FastAPI()

@app.get('/')
def main():
    return {"message" : 'Home'}

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class Frage(BaseModel):
   input: str

class Antwort(BaseModel):
   output : str

def stream_generator(prompt):
    try:
     response = client.models.generate_content_stream(
     model="gemini-2.5-flash", contents=prompt,
     config={
        "max_output_tokens" : 500
     }
     )

     for chunk in response:
       if chunk.text:
          print("Chunk" , chunk.text)
          yield chunk.text

    except Exception as error:
     yield f"Error : {str(error)}"
    
    
@app.post('/chat-stream')
def stream(data:Frage):

    prompt = f"""Explain clearly and shortly and at the end ask for follow up related Question
    
     User Question: 
     {data.input}
    """
    return StreamingResponse(
        stream_generator(prompt=prompt),
        media_type="text/plain"
    )
   