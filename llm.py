import json

from llama_cpp import Llama

llm = Llama(
    model_path="./models/mistral_7B_instruct_v02_Q8_0.gguf",
    chat_format="chatml",
    n_ctx=2048,
)

data = None
prompt = None

with open("data/csontvary.txt") as f:
    data = f.read()[:1000]

with open("prompts/test_prompt.txt") as f:
    prompt = f.read()

full_prompt = prompt.format(DATA=data)

output = llm.create_chat_completion(
    messages=[
        {"role": "user", "content": full_prompt},
    ],
    response_format={
        "type": "json_object",
    },
    temperature=0.7,
)

result = output["choices"][0]["message"]["content"]

print("*" * 50)
print(json.dumps(result, indent=4, ensure_ascii=False))
