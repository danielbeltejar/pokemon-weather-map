from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers.HealthRouter import health_router
from src.routers.TodayForecast import today_forecast_router

app = FastAPI()
app.include_router(health_router)
app.include_router(today_forecast_router)

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development
    allow_methods=["GET"],
    allow_headers=["*"],
)
