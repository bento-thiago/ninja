import datetime
from dateutil.relativedelta import relativedelta

def formataDataEntrada(data: str):
    data = datetime.datetime.strptime(data, '%d/%m/%Y')
    return data.strftime('%Y-%m-%d')


def formataDataSaida(data: datetime.datetime):
    return data.strftime('%d/%m/%Y')

def ultimoDiaMes(data:datetime.date):
    return (datetime.datetime(data.year, data.month, 1) + relativedelta(months=1) - relativedelta(days=1)).date()
