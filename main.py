import json
from contextlib import asynccontextmanager

from fastapi import FastAPI
from llama_cpp import Llama
from pydantic import BaseModel

import aisa

class Data(BaseModel):
    text: str
    prompt: str


model = None

def traverse_response(response):
    """
        Megtalalja es kinyeri az elso listat a dict tipusu adatbol
    """
    if isinstance(response, list):
        print(response)
        print("huha")
        for elem in response:
            yield elem
    elif isinstance(response, dict):
        yield from traverse_response(*response.values())
    else:
        print("ez nem jo", type(response))

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    # Load the LLM model
    model = Llama(
        model_path="./models/mistral_7B_instruct_v02_Q8_0.gguf",
        chat_format="chatml",
        n_ctx=2048,
    )
    yield

    # At shutdown: release the resources
    del model


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"model": model.tokenize(b"Hello World!")}


@app.post("/annot")
async def annot(data: Data):
    # TODO Pontos return type ?
    # TODO Error handling
    
    full_prompt = data.prompt.format(data.text)

    output = model.create_chat_completion(
        messages=[
            {"role": "user", "content": full_prompt},
        ],
        response_format={
            "type": "json_object",
        },
        temperature=0.7,
    )

    response = output["choices"][0]["message"]["content"]

    print(response)
    print("*"*30)

    try:
        response_json = json.loads(response)    
    except ValueError:
        print("Unable to load model response as JSON")
        return {} 

    entity_list = list(traverse_response(response_json))

    # TODO Nem robosztus! Nem szep!
    entity_list = [{"name" : list(e.values())[1], "tag" : list(e.values())[0]} for e in entity_list]

    annotated_text = aisa.annotate.create_annotations(data.text, entity_list)
    
    return annotated_text

@app.get("/train")
async def train():
    return {"message": "NOT IMPLEMENTED"}
