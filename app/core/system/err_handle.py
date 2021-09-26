import traceback

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import RequestValidationError
from starlette import status

from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse

from app.core.log.log_tools import LogTools
from app.core.settings.crud import settings


def run(app: FastAPI):
    if settings.value['err_test_mode']:
        @app.exception_handler(Exception)
        async def all_exception_handler(request, exc: Exception):
            """截取代码运行错误,并返回详细信息"""
            LogTools.e()
            return PlainTextResponse(f'{traceback.format_exc()}', 500)

        @app.exception_handler(HTTPException)
        async def custom_http_exception_handler(request: Request, exc: HTTPException):
            """过滤主动抛出的错误"""
            LogTools.e()
            # print(f'主动抛出{exc.status_code}错误')
            return await http_exception_handler(request, exc)

        @app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request: Request, exc: RequestValidationError):
            """过滤422的格式错误"""
            # return JSONResponse(
            #     status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            #     content=jsonable_encoder({
            #         "detail": exc.errors(),
            #         "body": exc.body,
            #         "quary": str(exc.args)
            #     }),
            # )
            rt = f'''
            发生了422错误,请对照文档和输入的参数,错误详情:
            422 エラーが発生しました、パラメータをチェックしてください
            {exc.errors()}
            -----
            
            你的body参数:
            bodyパラメータ：
            {exc.body}
            ---
            你的quary参数:
            quaryパラメータ:
            [{str(request.query_params)}]
            ---
            你的path参数:
            pathパラメータ：
            {request.path_params}
            '''
            return PlainTextResponse(rt, 422)
