import datetime as dt


class Record:
    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment

        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, self.DATE_FORMAT).date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
        today_amount = sum([
            record.amount
            for record in self.records
            if record.date == today
        ])

        return today_amount

    def get_week_stats(self):
        today = dt.date.today()
        week_ago = today - dt.timedelta(days=7)
        week_amount = float(sum([
            record.amount
            for record in self.records
            if record.date >= week_ago and record.date <= today]))

        return week_amount


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        left = self.limit - self.get_today_stats()
        if left > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {left} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    RUB_RATE = 1.0
    USD_RATE = 60.0
    EURO_RATE = 70.0

    def __init__(self, limit):
        super().__init__(limit)

    def get_today_cash_remained(self, currency):
        left = self.limit - self.get_today_stats()

        if left == 0:
            return 'Денег нет, держись'

        currencies = {
            'eur': ('Euro', self.EURO_RATE),
            'usd': ('USD', self.USD_RATE),
            'rub': ('руб', self.RUB_RATE),
        }

        cur, rate = currencies.get(currency)
        left = round(left / rate, 2)

        if left > 0:
            return f'На сегодня осталось {left} {cur}'

        left = abs(left)

        return f'Денег нет, держись: твой долг - {left} {cur}'


cash_calculator = CashCalculator(1000)

cash_calculator.add_record(Record(amount=145, comment="кофе"))

cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))

cash_calculator.add_record(Record(
    amount=3000, comment="бар в Танин др", date="08.11.2019"))

print(cash_calculator.get_today_cash_remained('rub'))
