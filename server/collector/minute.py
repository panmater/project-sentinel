from server.api.kis import KisClient


class MinuteCollector:

    def __init__(self):
        self.client = KisClient()

    def get(self, stock_code: str):
        minute_data = self.client.get_minute_chart(stock_code)

        return minute_data