import logging
from time import perf_counter
from typing import Callable

from fastapi import FastAPI, Response, Request

from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router

from app.core.config import get_settings #функция, возвращающая все настройки, в том числе cors_allow_origins

from app.core.logging import configure_logging
from starlette.middleware.base import RequestResponseEndpoint

configure_logging()

#получаю объект настроек, для того, чтобы корс пробросить
settings = get_settings() #возможно лучше просто импортировать settings из db.session


app = FastAPI() #объект фастапи (само приложение)


logger = logging.getLogger("app.middleware") # название логгера в логах    
#корс определяем, чтобы у fatapi было понимание, кто может подключаться и какие запросы, 
# с какими заголовкам отправлять нашему серверу (не рекомендуется ставиь в методс и хэдэр * на продакшне)
app.add_middleware(
    CORSMiddleware, 
    allow_origins = [
        settings.cors_allow_origins[0],
    ],
    allow_methods = ["*"],
    allow_headers = ["*"],
    allow_credentials = True,
)


cnt: int = 0

#log_requests выполнится до и после обработки каждого HTTP-запроса
@app.middleware("http") 
async def log_requests(request: Request, call_next: RequestResponseEndpoint) -> Response:
    started_at = perf_counter()
    try:
        response: Response = await call_next(request) #работа самого эндпоинта
    except Exception:
        duration_ms = (perf_counter() - started_at) * 1000
        logger.exception(
            "Request failed: %s %s completed_in=%.2fms",
            request.method,
            request.url.path,
            duration_ms,
        )
        raise

    duration_ms = (perf_counter() - started_at) * 1000
    logger.info(
        "%s %s -> %s (%.2f ms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response

@app.middleware("http")
async def http_counter(request: Request, callnext: RequestResponseEndpoint) -> Response:
    global cnt
    cnt+=1
    response: Response = await callnext(request)
    response.headers["X-Request-Number"] = str(cnt)
    return response

app.include_router(router=api_router) #пробрасываем наш роутер для тасок