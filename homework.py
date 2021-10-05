import datetime as dt


class Record:
    date_format = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment

        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, self.date_format).date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_time(self, days_count):
        a_days = 0
        past_t = dt.date.today() - dt.timedelta(days=days_count)
        today = dt.date.today()
        for i in self.records:
            if i.date > past_t and i.date <= today:
                a_days += i.amount
        return a_days

    def get_today_stats(self):
        return self.get_time(1)

    def get_week_stats(self) -> None:
        amount_last_7_days = []
        week_d = dt.date.today() - dt.timedelta(days=7)
        for record in self.records:
            if record.date > week_d and record.date <= dt.date.today():
                amount_last_7_days = amount_last_7_days.append(record)
        return sum(amount_last_7_days)


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

    def get_today_cash_remained(self, currency):
        left = self.limit - self.get_today_stats()

        currencies = {
            'rub': (self.RUB_RATE, 'Руб'),
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro')
        }
        currency_output = (
            f'{round(abs(left) / currencies[currency][0], 2)}'
            f'{currencies[currency][1]}'
        )

        if left == 0:
            return 'Денег нет, держись'
        elif left > 0:
            return f'На сегодня осталось {currency_output}'
        else:
            return f'Денег нет, держись: твой долг - {currency_output}'


cash_calculator = CashCalculator(1000)

cash_calculator.add_record(Record(amount=145, comment="кофе"))

cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))

cash_calculator.add_record(Record(
    amount=3000, comment="бар в Танин др", date="08.11.2019"))

print(cash_calculator.get_today_cash_remained('rub'))
