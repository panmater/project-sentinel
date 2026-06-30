class StateManager:
    def __init__(self):
        self.previous_states = {}

    def update(self, stock_code: str, current_data: dict, investor_data: dict | None = None):
        previous_data = self.previous_states.get(stock_code)

        self.previous_states[stock_code] = current_data

        return {
            "stock_code": stock_code,
            "previous": previous_data,
            "current": current_data,
            "investor": investor_data or {},
            "delta": self._calculate_delta(previous_data, current_data),
            "is_first_update": previous_data is None,
        }

    def _calculate_delta(self, previous_data: dict | None, current_data: dict):
        if previous_data is None:
            return None

        return {
            "price_delta": self._safe_subtract(
                current_data.get("current_price"),
                previous_data.get("current_price"),
            ),
            "volume_delta": self._safe_subtract(
                current_data.get("volume"),
                previous_data.get("volume"),
            ),
            "foreign_net_buy_delta": self._safe_subtract(
                current_data.get("foreign_net_buy_qty"),
                previous_data.get("foreign_net_buy_qty"),
            ),
            "program_net_buy_delta": self._safe_subtract(
                current_data.get("program_net_buy_qty"),
                previous_data.get("program_net_buy_qty"),
            ),
        }

    def _safe_subtract(self, current_value, previous_value):
        if current_value is None or previous_value is None:
            return None

        return current_value - previous_value