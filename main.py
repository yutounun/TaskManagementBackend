import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routes.api import router as api_router
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request
from db import engine

app = FastAPI()

# DB接続用のセッションクラス インスタンスが作成されると接続する
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

origins = ["http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

# Start the server when the code is executed
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, log_level="info", reload=True)
    print("running")


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    # each router will have request with state.db property
    request.state.db = SessionLocal()
    # proceed to the next middleware or the route handler
    response = await call_next(request)
    # route handler may return a response
    request.state.db.close()
    return response


# This file is main file on the top of every files
