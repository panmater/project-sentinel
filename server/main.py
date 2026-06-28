import time
import json
from pathlib import Path

from fastapi import FastAPI
from server.api.kis import KisClient
from server.state.state_manager import StateManager

app = FastAPI(
    title="Project Sentinel",
    description="AI Investment Assistant Server",
    version="0.1.0",
)

state_manager = StateManager()

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


@app.get("/watchlist")
def get_watchlist():
    watchlist_path = Path("watchlist.json")

    with open(watchlist_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


@app.get("/watchlist/prices")
def get_watchlist_prices():
    watchlist_path = Path("watchlist.json")

    with open(watchlist_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    client = KisClient()
    result = []

    for stock in data.get("stocks", []):
        try:
            price_data = client.get_stock_price(stock["code"])

            state = state_manager.update(
                stock_code=stock["code"],
                current_data=price_data,
            )

            result.append({
                "stock_code": stock["code"],
                "stock_name": stock["name"],

                "current_price": state["current"]["current_price"],
                "change_rate": state["current"]["change_rate"],
                "volume": state["current"]["volume"],

                "foreign_net_buy_qty": state["current"]["foreign_net_buy_qty"],
                "program_net_buy_qty": state["current"]["program_net_buy_qty"],

                "delta": state["delta"],
                "is_first_update": state["is_first_update"],
                "api_status": "success",
            })

        except Exception as error:
            result.append({
                "stock_code": stock["code"],
                "stock_name": stock["name"],
                "api_status": "error",
                "error_message": str(error),
            })

        time.sleep(0.2)

    return {
        "count": len(result),
        "stocks": result,
    }