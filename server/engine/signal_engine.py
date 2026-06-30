class SignalEngine:

    def calculate(self, features: dict | None, state: dict):
        if features is None:
            return None

        score = 0

        investor = state.get("investor", {})

        foreign_20d = investor.get("foreign_20d_sum", 0)

        if features["price_up"]:
            score += 15

        if features["volume_increasing"]:
            score += 20

        if features["foreign_buying"]:
            score += 25

        if foreign_20d > 1_000_000:
            score += 20

        elif foreign_20d > 0:
            score += 10

        if features["program_buying"]:
            score += 20

        if features["change_rate_positive"]:
            score += 10

        if features["foreign_holding_high"]:
            score += 10

        return {
            "score": score,
            "grade": self._grade(score)
        }

    def _grade(self, score):

        if score >= 90:
            return "S"

        if score >= 80:
            return "A"

        if score >= 70:
            return "B"

        if score >= 60:
            return "C"

        return "D"