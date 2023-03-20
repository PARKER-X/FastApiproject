from fastapi import FastAPI,Response,status,HTTPException
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
def get_post(id:int, response:Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id :{id} not found")
    
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message':f"post with id :{id} not found"}
    return {"post_detail":post}

def find_index_post(id):
    for i , p in enumerate(my_posts):
        if p["id"] == id:
            return i 

@app.delete('/posts/{id}')
def delete_post(id:int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f" id {id} does not exist")
    my_posts.pop(index)
    return {'message':"my post is succesfully deleted"}

@app.put('/posts/{id}')
def update_post(id:int,post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f" Post with id {id} does not exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'message': post_dict}


