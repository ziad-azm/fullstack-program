from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import ALLOWED_ORIGINS
from .database import init_db
from .routers.items import router as items_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Items API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items_router)


# ---------- Validation error handler (422 -> 400) ----------


def _field_message(field: str, error: dict) -> str:
    error_type = error.get("type", "")
    ctx = error.get("ctx", {})

    if error_type == "missing":
        return f"{field} is required"
    if error_type in ("greater_than", "greater_than_equal"):
        bound = ctx.get("gt", ctx.get("ge", 0))
        if isinstance(bound, float) and bound.is_integer():
            bound = int(bound)
        return f"{field} must be greater than {bound}"
    if error_type == "string_too_long":
        return f"{field} must be at most {ctx.get('max_length')} characters"
    if error_type == "string_too_short":
        return f"{field} must not be empty"
    if error_type in ("float_parsing", "float_type", "int_parsing", "int_type"):
        return f"{field} must be a number"
    if error_type in ("bool_parsing", "bool_type"):
        return f"{field} must be a boolean"
    if error_type == "json_invalid":
        return "request body must be valid JSON"
    return error.get("msg", f"{field} is invalid")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        loc = [str(part) for part in err.get("loc", []) if part not in ("body", "query", "path")]
        field = loc[-1] if loc else "body"
        errors.append({"field": field, "message": _field_message(field, err)})
    return JSONResponse(status_code=400, content={"detail": errors})
