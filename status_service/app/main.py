import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy import null
from sqlalchemy.orm import Session
from collections import Counter

from database import database as database
from database.database import Plane

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'service alive'}


@app.post("/set_status")
async def set_status(plane_id: int, status: str, db: db_dependency):
    try:
        plane_db = db.query(Plane).filter(Plane.id == plane_id).first()
        plane_db.status = status
        db.commit()
        db.refresh(plane_db)
        return "Success"
    except Exception as e:
        raise HTTPException(status_code=404, detail="Planes not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
