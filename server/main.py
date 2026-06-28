from fastapi import FastAPI
from server.api.kis import KisClient

app = FastAPI(
    title="Project Sentinel",
    description="AI Investment Assistant Server",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "project": "Project Sentinel",
        "status": "running",
        "message": "Sentinel Engine is alive.",
    }


@app.get("/kis/token-test")
def kis_token_test():
    client = KisClient()
    token_data = client.get_access_token()

    return {
        "status": "success",
        "token_type": token_data.get("token_type"),
        "expires_in": token_data.get("expires_in"),
        "access_token_exists": bool(token_data.get("access_token")),
    }


@app.get("/stocks/{stock_code}/price")
def get_stock_price(stock_code: str):
    client = KisClient()
    return client.get_stock_price(stock_code)