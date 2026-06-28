class SignalEngine:

    def calculate(self, features: dict | None):

        if features is None:
            return None

        score = 0

        if features["price_up"]:
            score += 15

        if features["volume_increasing"]:
            score += 20

        if features["foreign_buying"]:
            score += 25

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