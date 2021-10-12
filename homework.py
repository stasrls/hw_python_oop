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
        today_amount = sum([
            record.amount
            for record in self.records
            if record.date == dt.date.today()
        ])

        return today_amount

    def get_week_stats(self):
        week_ago = dt.date.today() - dt.timedelta(days=7)
        week_amount = float(sum([
            record.amount
            for record in self.records
            if week_ago <= record.date <= dt.date.today()]))

        return week_amount

    def left_fun(self):
        left = self.limit - self.get_today_stats()

        return left


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        left_cal = self.left_fun()
        if left_cal > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {left_cal} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    RUB_RATE = 1.0
    USD_RATE = 60.0
    EURO_RATE = 70.0

    def get_today_cash_remained(self, currency) -> str:
        left = self.left_fun()

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
