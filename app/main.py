from fastapi import FastAPI
from . import models, schema, utils
from .database import engine, SessionLocal , get_db
from .routers import post, user, auth, vote
from .config import settings


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()




# class Post(BaseModel):
#     title: str 
#     content: str
#     published: bool = True
    # rating: Optional[int] = None


# Database Connection
# try:
#     conn = psycopg2.connect(host="localhost", database='fastapi', user='postgres', password = 'password123', cursor_factory = RealDictCursor)
#     cursor = conn.cursor()
#     print("Database connection was succesfull!")
# except Exception as error:
#     print("Failed to connect database")
#     print("Error:",error)
#     time.sleep(2)



# my_posts = []

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p
        
# @app.get('/')
# async def root():
#     context = {"message":"Hello World"}
#     return context


# @app.get("/sqlalchemy")
# def tests_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     print(posts)
#     return {"data":posts}


# @app.get("/posts", response_model=List[schema.Post])
# def get_posts(db: Session = Depends(get_db)):
#     # SQL
#     # posts = cursor.execute(""" SELECT * FROM posts""")
#     # posts = cursor.fetchall()
#     posts = db.query(models.Post).all()
#     return posts

# @app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
# def create_posts(post: schema.PostCreate, db:Session= Depends(get_db)):
#     # Manual using list
#     # post_dict = post.dict()
#     # post_dict['id']  = randrange(0,1000)
#     # my_posts.append(post_dict)
#     # print(post)
#     # return {"data":post}

#     # Use Sql
#     # cursor.execute(""" INSERT INTO  posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
#     # new_post = cursor.fetchone()
#     # conn.commit()

#     new_post = models.Post(title = post.title, content = post.content, published= post.published)


#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)

#     return new_post


# @app.get('/posts/{id}')
# def get_post(id:int, response:Response, db: Session= Depends(get_db)):
#     # Sql
#     # cursor.execute(""" SELECT * from posts WHERE id = %s """, (str(id)))
#     # post = cursor.fetchone()
#     # print(post)

#     post = db.query(models.Post).filter(models.Post.id==id).first()
    
   

#     if not post:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
#                             detail = f"post with id :{id} not found")
    
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {'message':f"post with id :{id} not found"}
#     return {"post_detail":post}

# # def find_index_post(id):
# #     for i , p in enumerate(my_posts):
# #         if p["id"] == id:
# #             return i 

# @app.delete('/posts/{id}')
# def delete_post(id:int, db: Session=Depends(get_db)):
#     # Manual
#     # index = find_index_post(id)

#     # Sql
#     # cursor.execute(""" DELETE from posts WHERE id = %s RETURNING * """, (str(id)))
#     # deleted_post = cursor.fetchone()
#     # conn.commit()

#     deleted_post = db.query(models.Post).filter(models.Post.id==id)

#     if deleted_post.first() == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail = f" id {id} does not exist")
#     # my_posts.pop(index)
#     deleted_post.delete(synchronize_session=False)
#     db.commit()
#     return {'message':"my post is succesfully deleted"}

# @app.put('/posts/{id}',response_model=schema.Post)
# def update_post(id:int,ppost: schema.PostCreate, db:Session=Depends(get_db)):
#     # Manual
#     # index = find_index_post(id)

#     # Sql
#     # cursor.execute(""" UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RETURNING * """, (post.title,post.content,post.published,str(id)))
#     # updated_post = cursor.fetchone()
#     # conn.commit()

#     post_query = db.query(models.Post).filter(models.Post.id==id)
#     updated_post = post_query.first()


#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail = f" Post with id {id} does not exist")
#     # post_dict = post.dict()
#     # post_dict['id'] = id
#     # my_posts[index] = post_dict

#     post_query.update(ppost.dict(), synchronize_session=False)
#     db.commit()
#     return {'message': post_query.first()}

# @app.post("/users", status_code=status.HTTP_201_CREATED)
# def create_user(user: schema.UserCreate, db:Session=Depends(get_db)):

#     # Hash the Password - user.password
#     hashed_password = utils.hash(user.password)
#     user.password = hashed_password
    
#     new_user = models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)


#     return new_user

# @app.get('/users/{id}', response_model = schema.Userout)
# def get_user(id:int,db:Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()

#     if not user:
#         raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"User od: {id} does not exist")

#     return user