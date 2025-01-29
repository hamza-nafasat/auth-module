from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from routes.user_routes import router as user_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(user_router)


# Global error handler
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={  # ✅ Custom JSON structure
            "success": False,
            "message": (
                exc.detail if isinstance(exc.detail, str) else "An error occurred"
            ),
        },
    )
