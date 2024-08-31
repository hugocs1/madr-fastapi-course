from fastapi import FastAPI, status

from madr.routers import auth, authors, users
from madr.schemas.health_check import HealthCheck

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(authors.router)


@app.get(
    '/health',
    tags=['healthcheck'],
    summary='Perform a Health Check',
    response_description='Return HTTP Status Code 200 (OK)',
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    return HealthCheck(status='OK')
