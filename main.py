from fastapi import FastAPI
from fetch import fetch, get_connections

app = FastAPI()

@app.get('/analyze/github/trending/{language}')
async def oh_yeah(language: str):
    url = f'https://github.com/trending/{language}?since=daily'
    data = fetch(url)
    data = get_connections(data)
    return data
#pickup your phone