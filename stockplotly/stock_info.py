from enum import Flag
import yahoo_fin.stock_info as si
import plotly.express as px

class Stock():

    def __init__(self, ticker, start_date, end_date):
        self.__ticker = ticker
        self.__start_date = start_date
        self.__end_date = end_date
        self.__history_price = si.get_data(
            ticker, 
            start_date=start_date, 
            end_date=end_date, 
            index_as_date=False,
            )

    def history_price(self):
        print(self.__history_price)
