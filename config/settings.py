import os, json, datetime

class Settings:
    # Small token numbers used here represent logical tokens; billing control is conceptual.
    DAILY_TOKEN_LIMIT = int(os.environ.get('DAILY_TOKEN_LIMIT', '1600'))
    MONTHLY_TOKEN_CAP = float(os.environ.get('MONTHLY_TOKEN_CAP', '50.0'))
    STORAGE_FILE = os.environ.get('TOKEN_USAGE_FILE', r'C:\LEVEL14\token_usage.json')

class TokenLimiter:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.file = self.settings.STORAGE_FILE
        # initialize storage
        if not os.path.exists(self.file):
            with open(self.file, 'w') as f:
                json.dump({'month': self._current_month(), 'used': 0.0}, f)

    def _current_month(self):
        now = datetime.datetime.utcnow()
        return f"{now.year}-{now.month:02d}"

    def get_monthly_usage(self):
        with open(self.file, 'r') as f:
            data = json.load(f)
        if data.get('month') != self._current_month():
            return 0.0
        return data.get('used', 0.0)

    def add_usage(self, amount):
        with open(self.file, 'r') as f:
            data = json.load(f)
        if data.get('month') != self._current_month():
            data = {'month': self._current_month(), 'used': 0.0}
        data['used'] = data.get('used', 0.0) + float(amount)
        with open(self.file, 'w') as f:
            json.dump(data, f)

    def allow_request(self, cost_units):
        # cost_units is a small integer representing the relative cost for the request
        # Convert monthly cap to conceptual units: here 1 unit ~ very small cost
        monthly_used = self.get_monthly_usage()
        if monthly_used + cost_units > self.settings.MONTHLY_TOKEN_CAP:
            return False
        # also check daily limit (not tracked per-day in this simple file-based limiter)
        # we just allow based on monthly cap to ensure hard stop behavior
        self.add_usage(cost_units)
        return True
