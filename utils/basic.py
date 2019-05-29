from datetime import datetime
from random import randint


class Basic():

    def gdfs(self, str_date):  # get date from string
        return datetime.strptime(str_date, '%d/%m/%Y').date()

    def random_with_n_digits(self, n):
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1
        return randint(range_start, range_end)

    def diff_month(self, d1, d2):
        return (d1.year - d2.year) * 12 + d1.month - d2.month
