from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .api import horoscope, matchmaking, reports, translations, places
from .db.session import engine
from .models import Base
from .core.config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(horoscope.router, prefix="/api/horoscope", tags=["horoscope"])
app.include_router(matchmaking.router, prefix="/api/matchmaking", tags=["matchmaking"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])
app.include_router(translations.router, prefix="/api/translations", tags=["translations"])
app.include_router(places.router, prefix="/api/places", tags=["places"])

@app.get("/")
async def root():
    return {"message": "Welcome to Epic-X Horoscope API"}
