from server.api.kis import KisClient


class InvestorCollector:

    def __init__(self):
        self.client = KisClient()

    def get(self, stock_code: str):
        investor_data = self.client.get_investor_trend(stock_code)
        history = investor_data.get("history", [])

        return {
            "stock_code": stock_code,
            "foreign_5d_sum": self._sum_recent(history, "foreign_net_buy_qty", 5),
            "foreign_20d_sum": self._sum_recent(history, "foreign_net_buy_qty", 20),
            "institution_5d_sum": self._sum_recent(history, "institution_net_buy_qty", 5),
            "institution_20d_sum": self._sum_recent(history, "institution_net_buy_qty", 20),
            "individual_5d_sum": self._sum_recent(history, "individual_net_buy_qty", 5),
            "individual_20d_sum": self._sum_recent(history, "individual_net_buy_qty", 20),
            "api_status": investor_data.get("api_status"),
        }

    def _sum_recent(self, history: list, key: str, days: int):
        recent_rows = history[:days]

        total = 0

        for row in recent_rows:
            value = row.get(key)

            if value is not None:
                total += value

        return total