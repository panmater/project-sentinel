class FeatureEngine:

    def analyze(self, state: dict):

        if state["is_first_update"]:
            return None

        delta = state["delta"]
        current = state["current"]

        features = {

            "price_up": delta["price_delta"] > 0,

            "price_down": delta["price_delta"] < 0,

            "volume_increasing": delta["volume_delta"] > 0,

            "foreign_buying": delta["foreign_net_buy_delta"] > 0,

            "program_buying": delta["program_net_buy_delta"] > 0,

            "change_rate_positive": current["change_rate"] > 0,

            "foreign_holding_high":
                (current["foreign_holding_rate"] or 0) >= 30,

        }

        return features