from fastapi import FastAPI
from fetch import fetch, get_connections
import time

app = FastAPI()

@app.get('/analyze/github/trending/{language}')
async def oh_yeah(language: str):
    # x = time.time()
    url = f'https://github.com/trending/{language}?since=daily'
    data = fetch(url)
    data = get_connections(data)
    # y = time.time()
    # print(y-x)
    return data
#pickup your phone