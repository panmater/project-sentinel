class FeatureEngine:

    def analyze(self, state: dict):

        if state["is_first_update"]:
            return None

        delta = state["delta"]
        current = state["current"]
        minute = state.get("minute", {})

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

        investor = state.get("investor", {})

        features.update({

            "foreign_5d_buying":
                investor.get("foreign_5d_sum", 0) > 0,

            "foreign_20d_buying":
                investor.get("foreign_20d_sum", 0) > 0,

            "institution_5d_buying":
                investor.get("institution_5d_sum", 0) > 0,

            "institution_20d_buying":
                investor.get("institution_20d_sum", 0) > 0,

            "individual_5d_buying":
                investor.get("individual_5d_sum", 0) > 0,

            "individual_20d_buying":
                investor.get("individual_20d_sum", 0) > 0,

            "minute_price_up":
                minute.get("recent_price_direction") == "up",

            "minute_price_down":
                minute.get("recent_price_direction") == "down",

            "minute_volume_surge":
                minute.get("volume_surge", False),

        })

        return features