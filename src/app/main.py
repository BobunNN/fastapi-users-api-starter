import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # noqa


# Basic logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

app = FastAPI()

# Optional: Enable CORS (uncomment to use)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Adjust as needed
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.get("/")
def root() -> str:
    logging.info("Health check endpoint called.")
    return "ok"
