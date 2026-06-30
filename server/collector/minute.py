from server.api.kis import KisClient


class MinuteCollector:

    def __init__(self):
        self.client = KisClient()

    def get(self, stock_code: str):
        minute_data = self.client.get_minute_chart(stock_code)
        candles = minute_data.get("candles", [])

        recent_5 = candles[:5]
        recent_20 = candles[:20]

        return {
            "stock_code": stock_code,
            "recent_price_direction": self._price_direction(recent_5),
            "recent_5_volume_sum": self._volume_sum(recent_5),
            "recent_20_volume_avg": self._volume_avg(recent_20),
            "volume_surge": self._is_volume_surge(recent_5, recent_20),
            "api_status": minute_data.get("api_status"),
        }

    def _price_direction(self, candles: list):
        if len(candles) < 2:
            return "unknown"

        latest_price = candles[0].get("price")
        past_price = candles[-1].get("price")

        if latest_price is None or past_price is None:
            return "unknown"

        if latest_price > past_price:
            return "up"

        if latest_price < past_price:
            return "down"

        return "flat"

    def _volume_sum(self, candles: list):
        return sum((candle.get("volume") or 0) for candle in candles)

    def _volume_avg(self, candles: list):
        if not candles:
            return 0

        return self._volume_sum(candles) / len(candles)

    def _is_volume_surge(self, recent_5: list, recent_20: list):
        recent_5_avg = self._volume_avg(recent_5)
        recent_20_avg = self._volume_avg(recent_20)

        if recent_20_avg == 0:
            return False

        return recent_5_avg >= recent_20_avg * 1.5