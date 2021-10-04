import datetime as dt


class Record:
    date_format = '%d.%m.%Y'

    def __init__(self, amount, comment, date=dt.date.today()):
        self.amount = amount
        self.comment = comment
        if isinstance(date, dt.date):
            self.date = date
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

    def get_week_stats(self):
        return self.get_time(7)


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        spent = self.get_today_stats()
        left = self.limit - spent
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
        spent = self.get_today_stats()
        left = self.limit - spent

        currencies = {
            'rub': (self.RUB_RATE, 'Руб'),
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro')
        }
        currency_out = (f'{round(abs(left) / currencies[currency][0], 2)} '
                        f'{currencies[currency][1]}')

        if left == 0:
            return 'Денег нет, держись'
        if left < 0:
            return (f'Денег нет, держись: твой долг - {currency_out}')

        return (f'На сегодня осталось {currency_out}')


cash_calculator = CashCalculator(1000)

cash_calculator.add_record(Record(amount=145, comment="кофе"))

cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))

cash_calculator.add_record(Record(
    amount=3000, comment="бар в Танин др", date="08.11.2019"))

print(cash_calculator.get_today_cash_remained('rub'))
