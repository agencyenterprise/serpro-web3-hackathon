import traceback
from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.routing import APIRoute
from app.logger import logger


class PyColors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class ExceptionHandlingRouter(APIRoute):
    def get_route_handler(self):
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except HTTPException as http_error:
                logger.warning(
                    "%s(%s) - %s%s",
                    PyColors.WARNING,
                    http_error.status_code,
                    http_error.detail,
                    PyColors.ENDC,
                )

                raise http_error

            except Exception as error:
                logger.error(
                    "%s%s%s", PyColors.FAIL, traceback.format_exc(), PyColors.ENDC
                )

                raise HTTPException(
                    status_code=500, detail=f"Internal Server Error - {error}"
                ) from error

        return custom_route_handler


def get_router():
    return APIRouter(route_class=ExceptionHandlingRouter)
