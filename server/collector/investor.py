from server.api.kis import KisClient


class InvestorCollector:

    def __init__(self):
        self.client = KisClient()

    def get(self, stock_code: str):
        """
        종목별 투자자 수급
        (외국인 / 기관 / 개인)
        """
        pass