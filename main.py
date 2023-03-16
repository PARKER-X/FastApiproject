from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

my_posts = []


class Post(BaseModel):
    title: str 
    content: str
    published: bool = True
    rating: Optional[int] = None




def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
@app.get('/')
async def root():
    context = {"message":"Hello World"}
    return context

@app.get("/posts")
def get_posts():
    return {"data":my_posts}

@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id']  = randrange(0,1000)
    my_posts.append(post_dict)
    print(post)
    return {"data":post}


@app.get('/posts/{id}')
def get_post(id:int):
    post = find_post(id)
    return {"post_detail":post}


