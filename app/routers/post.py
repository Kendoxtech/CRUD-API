from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from ..db import   get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
 


router = APIRouter( tags=['Post'])





@router.post("/createpost", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   # cursor.execute(""" INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
   #                 (post.title, post.content, post.published))
   # new_post = cursor.fetchone()
    
    print(current_user.email)
    new_post = models.Post(owner_id =current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/posts", response_model=List[schemas.VoteOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 1, skip: int = 0, search: Optional[str] = ""):
    print(limit)
    print(search)
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count( models.Vote.post_id).label("vote")).join(models.Vote, models.Vote.post_id == models.Post.id,
                                                                                             isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
  #  result = db.query(models.Post).join(models.Vote, models.Vote.post_id == models.Post.id,
  #                                                                                           isouter=True)
    
    return posts 


@router.get("/posts/{id}", response_model=schemas.VoteOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute(""" SELECT * FROM post where id = %s  """, (str(id)))
   # post = cursor.fetchone()
   # post = find_post(id)"""  """
    # posts = db.query(models.Post).filter(models.Post.id == id).first()
    print(current_user)
    post = db.query(models.Post, func.count( models.Vote.post_id).label("vote")).join(models.Vote, models.Vote.post_id == models.Post.id,
                                                                                             isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
   
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")
   # if post.owner_id != current_user.id:
   #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Action not allowed")
    
   
    return post



@router.get("/postss/latest", response_model=List[schemas.PostResponse])
def get_latest_post(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    print(user_id)
    
    #cursor.execute(""" SELECT * FROM post """)
   # posts = cursor.fetchall()
   # posts = my_posts[len(my_posts)-1]
    posts = db.query(models.Post).all()
    db.commit()
    
    return posts

@router.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.UpdatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute(""" UPDATE  post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
   #                 (post.title, post.content, post.published, (str(id))))
   # updated_post = cursor.fetchone()
   # conn.commit()
    print(current_user)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Action not allowed")
    post_query.update(updated_post.model_dump(),synchronize_session=False)
    db.commit()
    
    return post_query.first()



@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   # cursor.execute(""" DELETE  FROM post WHERE id = %s RETURNING * """, (str(id),))
  #  deleted_posts = cursor.fetchone()
   # conn.commit()
    print(current_user)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {id} does not exist')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Action not allowed")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)