import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Form
from typing import Annotated
from keycloak import KeycloakOpenID
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

KEYCLOAK_URL = "http://keycloak:8080/"
KEYCLOAK_CLIENT_ID = "test"
KEYCLOAK_REALM = "myRealm"
KEYCLOAK_CLIENT_SECRET = "zXkxCT1zhllUO1t6KqPC8qREQKklFNMM"

user_token = ""
keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_URL,
                                  client_id=KEYCLOAK_CLIENT_ID,
                                  realm_name=KEYCLOAK_REALM,
                                  client_secret_key=KEYCLOAK_CLIENT_SECRET)

###########
#Prometheus
from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    try:
        # Получение токена
        token = keycloak_openid.token(grant_type=["password"],
                                      username=username,
                                      password=password)
        global user_token
        user_token = token
        return token
    except Exception as e:
        print(e)  # Логирование для диагностики
        raise HTTPException(status_code=400, detail="Не удалось получить токен")

def user_got_role():
    global user_token
    token = user_token
    try:
        userinfo = keycloak_openid.userinfo(token["access_token"])
        token_info = keycloak_openid.introspect(token["access_token"])
        if "myRole" not in token_info["realm_access"]["roles"]:
            raise HTTPException(status_code=403, detail="Access denied")
        return token_info
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token or access denied")

@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    if (user_got_role()):
        return {'message': 'service alive'}
    else:
        return "Wrong JWT Token"


@app.post("/add_plane")
async def add_plane(plane: PlaneModel, db: db_dependency):
    if (user_got_role()):
        plane_db = Plane(airplane_name=plane.airplane_name,
                         num_seats=plane.num_seats)
        try:
            db.add(plane_db)
            db.commit()
            db.refresh(plane_db)
            return "Success"
        except Exception as e:
            return "Cant add plane"
    else:
        return "Wrong JWT Token"

@app.get("/get_planes")
async def get_planes(db: db_dependency):
    if (user_got_role()):
        try:
            result = db.query(Plane).filter().all()
            return result
        except Exception as e:
            raise HTTPException(status_code=404, detail="Planes not found")
    else:
        return "Wrong JWT Token"

@app.get("/get_plane_by_id")
async def get_plane_by_id(plane_id: int, db: db_dependency):
    if (user_got_role()):
        try:
            result = db.query(Plane).filter(Plane.id == plane_id).first()
            return result
        except Exception as e:
            raise HTTPException(status_code=404, detail="Plane not found")
    else:
        return "Wrong JWT Token"

@app.get("/get_planes_by_name")
async def get_planes_by_name(plane_name: str, db: db_dependency):
    if (user_got_role()):
        try:
            result = db.query(Plane).filter(Plane.airplane_name == plane_name).first()
            return result
        except Exception as e:
            raise HTTPException(status_code=404, detail="Messages not found")
    else:
        return "Wrong JWT Token"

@app.delete("/delete_plane")
async def delete_plane(plane_id: int, db: db_dependency):
    if (user_got_role()):
        try:
            plane = db.query(Plane).filter(Plane.id == plane_id).first()
            db.delete(plane)
            db.commit()
            return "Success"
        except Exception as e:
            return "Cant find plane"
    else:
        return "Wrong JWT Token"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
