from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from .. import schemas, db, models, oauth2
from sqlalchemy.orm import Session
from ..db import get_db


router = APIRouter(tags=['Vote'])


@router.post("/votes", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(db.get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {vote.post_id} does not exist")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} already voted on post {vote.post_id}")
        new_vote =  models.Vote(post_id= vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
       
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}



@router.get("/votes")
def get_votes(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    print(user_id)
    
    #cursor.execute(""" SELECT * FROM post """)
   # posts = cursor.fetchall()
   # posts = my_posts[len(my_posts)-1]
    votes = db.query(models.Vote).all()
    db.commit()
    return votes