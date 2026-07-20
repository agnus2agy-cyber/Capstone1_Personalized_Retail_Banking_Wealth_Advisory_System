

from fastapi import FastAPI

from routes.query_routes import router as query_router


app = FastAPI(
	title="Retail Banking & Wealth Advisory System",
	version="1.0"
)


@app.get("/")
def root():
	return {
    	"message": "Retail Banking & Wealth Advisory System"
	}


@app.get("/health")
def health():
	return {
    	"status": "UP"
	}


app.include_router(query_router)


