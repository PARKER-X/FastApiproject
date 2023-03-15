from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def root():
    context = {"message":"Hello World"}
    return context