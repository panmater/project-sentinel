import os
import requests
from dotenv import load_dotenv

load_dotenv()


class KisClient:
    access_token_cache = None
    def __init__(self):
        self.app_key = os.getenv("KIS_APP_KEY")
        self.app_secret = os.getenv("KIS_APP_SECRET")
        self.base_url = "https://openapi.koreainvestment.com:9443"

    def get_access_token(self):
        if KisClient.access_token_cache:
            return KisClient.access_token_cache

        url = f"{self.base_url}/oauth2/tokenP"

        payload = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
        }

        response = requests.post(url, json=payload)
        response.raise_for_status()

        token_data = response.json()
        KisClient.access_token_cache = token_data.get("access_token")

        return KisClient.access_token_cache

    def get_token_info(self):
        token = self.get_access_token()

        return {
            "access_token_exists": bool(token),
            "token_cached": True,
        }

    def get_stock_price(self, stock_code: str):
        access_token = self.get_access_token()

        url = f"{self.base_url}/uapi/domestic-stock/v1/quotations/inquire-price"

        headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {access_token}",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "tr_id": "FHKST01010100",
        }

        params = {
            "fid_cond_mrkt_div_code": "J",
            "fid_input_iscd": stock_code,
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        raw_data = response.json()
        output = raw_data.get("output") or raw_data.get("출력") or {}

        return self._format_stock_price(stock_code, output)

    def _to_int(self, value):
        if value in [None, ""]:
            return None
        return int(float(str(value).replace(",", "").strip()))

    def _to_float(self, value):
        if value in [None, ""]:
            return None
        return float(str(value).replace(",", "").strip())

    def _flow_label(self, value):
        number = self._to_int(value)

        if number is None:
            return "no_data"
        if number > 0:
            return "net_buy"
        if number < 0:
            return "net_sell"
        return "neutral"

    def _format_stock_price(self, stock_code: str, output: dict):
        return {
            "stock_code": stock_code,
            "market": output.get("rprs_mrkt_kor_name"),
            "sector": output.get("bstp_kor_isnm") or output.get("bstp_kor_isn m"),

            "current_price": self._to_int(output.get("stck_prpr")),
            "change_price": self._to_int(output.get("prdy_vrss")),
            "change_rate": self._to_float(output.get("prdy_ctrt")),

            "open_price": self._to_int(output.get("stck_oprc")),
            "high_price": self._to_int(output.get("stck_hgpr")),
            "low_price": self._to_int(output.get("stck_lwpr")),
            "base_price": self._to_int(output.get("stck_sdpr")),

            "volume": self._to_int(output.get("acml_vol")),
            "trading_value": self._to_int(output.get("acml_tr_pbmn")),

            "foreign_holding_rate": self._to_float(output.get("hts_frgn_ehrt")),
            "foreign_net_buy_qty": self._to_int(output.get("frgn_ntby_qty")),
            "foreign_flow": self._flow_label(output.get("frgn_ntby_qty")),

            "program_net_buy_qty": self._to_int(output.get("pgtr_ntby_qty")),
            "program_flow": self._flow_label(output.get("pgtr_ntby_qty")),

            "per": self._to_float(output.get("per")),
            "pbr": self._to_float(output.get("pbr")),
            "eps": self._to_float(output.get("eps")),
            "bps": self._to_float(output.get("bps")),

            "week_52_high": self._to_int(output.get("w52_hgpr")),
            "week_52_low": self._to_int(output.get("w52_lwpr")),

            "api_status": "success",
        }