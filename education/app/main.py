from fastapi import FastAPI
import uvicorn
from app.tutorials.router import router as task_router
from starlette.middleware.cors import CORSMiddleware
from app.users.router import router as user_router
from app.email_templates.router import router as email_router
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


from redis import asyncio as aioredis

app = FastAPI()

app.include_router(router=task_router)
app.include_router(router=user_router)
app.include_router(router=email_router)
# Подключение CORS, чтобы запросы к API могли приходить из браузера

origins = [
    # 3000 - порт, на котором работает фронтенд на React.js
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin",
                   "Authorization"]
)


# @app.on_event("startup")
# async def startup():
#     redis = await aioredis.create_redis_pool("redis://localhost", encoding="utf8")
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


if __name__ == "__main__":
    uvicorn.run(app="app.main:app", reload=True, port=3000, host="localhost")

