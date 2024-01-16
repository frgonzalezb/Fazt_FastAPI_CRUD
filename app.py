import os
import uvicorn

from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Text
from uuid import uuid4 as uuid


app = FastAPI()
load_dotenv()

posts = []
lorem = 'Proident sint dolore dolore ipsum do est.'


# Models
class Post(BaseModel):
    id: Optional[str] = str(uuid())         # optional attr value example
    title: Optional[str] = lorem            # if opt, attr needs default
    author: str
    content: Text
    created_at: datetime = datetime.now()   # default attr value example
    published_at: datetime
    is_published: bool = False              # default attr value example


# Views
@app.get('/')
def read_root():
    return {'welcome': 'Welcome to my API!'}


@app.get('/posts')
def list_posts():
    return posts


@app.post('/posts')
def create_post(post: Post):
    posts.append(post.model_dump()) # dict() is deprecated!
    # return 'Received!'
    return posts[-1]


@app.get('/posts/{id}')
def read_post(id: str):
    for post in posts:
        if post['id'] == id:
            return post
    raise HTTPException(status_code=404, detail='Post not found!')


@app.delete('/posts/{id}')
def destroy_post(id: str):
    for index, post in enumerate(posts):
        if post['id'] == id:
            posts.pop(index)
            return {'msg': 'Post has been deleted successfully!'}
    raise HTTPException(status_code=404, detail='Post not found!')


@app.put('/posts/{id}')
def update_post(id: str, updated_post: Post):
    for index, post in enumerate(posts):
        if post['id'] == id:
            posts[index]['title'] = updated_post.title
            posts[index]['author'] = updated_post.author
            posts[index]['content'] = updated_post.content
            return {'msg': 'Post has been updated successfully!'}
    raise HTTPException(status_code=404, detail='Post not found!')


# Main
if __name__ == '__main__':
    uvicorn.run(
        app=os.environ['APP'], 
        host=os.environ['HOST'], 
        port=int(os.environ['PORT']), 
        reload=eval(os.environ['RELOAD'])
    )
