import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Form
from typing import Annotated

from sqlalchemy.orm import Session

from database import database as database
from database.database import Plane
from model.plane import PlaneModel

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


@app.post("/add_plane")
async def add_plane(plane: PlaneModel, db: db_dependency):
    plane_db = Plane(airplane_name=plane.airplane_name,
                     num_seats=plane.num_seats)
    try:
        db.add(plane_db)
        db.commit()
        db.refresh(plane_db)
        return "Success"
    except Exception as e:
        return "Cant add plane"


@app.get("/get_planes")
async def get_planes(db: db_dependency):
    try:
        result = db.query(Plane).filter().all()
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail="Planes not found")


@app.get("/get_plane_by_id")
async def get_plane_by_id(plane_id: int, db: db_dependency):
    try:
        result = db.query(Plane).filter(Plane.id==plane_id).all()
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail="Plane not found")


@app.get("/get_planes_by_name")
async def get_planes_by_name(plane_name: str, db: db_dependency):
    try:
        result = db.query(Plane).filter(Plane.name==plane_name).all()
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail="Messages not found")

@app.delete("/delete_plane")
async def delete_plane(plane_id: int, db: db_dependency):
    try:
        plane = db.query(Plane).filter(Plane.id == plane_id).first()
        db.delete(plane)
        db.commit()
        return "Success"
    except Exception as e:
        return "Cant find plane"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
