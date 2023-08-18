from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..import database, models, schemas, utils, oauth2

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # Check whether post with the given id (in the request body) exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {vote.post_id} does not exist")
    
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    # Is user want to like (vote.dir = 1)
    if (vote.dir == 1):
        # Is there a vote entity made by the current user to the current post already? Then don't allow
        if (found_vote):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on the post {vote.post_id}")

        # Add the vote to the DB
        new_vote = models.Vote(post_id=vote.post_id,
                               user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}

    # Is user want to revert his like back (vote.dir = 0)
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Vote does not exist")

        # Delete vote from the DB
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}
