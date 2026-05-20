class ChurnCalculator:
    def calculate_risk(self, mrr, prev_mrr=None, slack_msgs=0):
        score = 50
        if prev_mrr and mrr < prev_mrr * 0.95:
            score -= 10
        if slack_msgs < 10:
            score += 20
        score = max(0, min(100, score))
        return score

    def get_risk_level(self, score):
        if score < 30:
            return "LOW"
        elif score < 70:
            return "MEDIUM"
        else:
            return "HIGH"