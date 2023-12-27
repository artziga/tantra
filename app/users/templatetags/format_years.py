import datetime
from datetime import date

from django import template

register = template.Library()



@register.filter
def years_suffix(value):
    if value is None or value == '':
        return
    if value % 10 == 1 and value % 100 != 11:
        suffix = "год"
    elif value % 10 in [0, 2, 3, 4] and value % 100 not in [12, 13, 14]:  # тут 0 потому что указывается <1 года
        suffix = "года"
    else:
        suffix = "лет"

    return suffix


@register.filter
def format_years(value):
    suffix = years_suffix(value)
    return f"{value} {suffix}"


@register.filter
def years_from_date(input_date):
    if not input_date:
        return
    today = date.today()
    try:
        the_day = input_date.replace(year=today.year)
    except ValueError:  # raised when birth date is February 29 and the current year is not a leap year
        the_day = input_date.replace(year=today.year, month=input_date.month + 1, day=1)
    if the_day > today:
        return today.year - input_date.year - 1
    else:
        return today.year - input_date.year
