# -*- coding: utf-8 -*-

import stockplotly.stock_draw as sd
import time

def main():
    #stock parameter
    ticker = 'tsla'
    startdate = '01/01/2020'
    enddate = '09/04/2022'
    io = True

    stock = sd.Stock(ticker, startdate, enddate, io_image=io)
    stock.history_price()
    stock.history_price_area()
    stock.candlestick()
    stock.ohlc()
    stock.compare_index()
    stock.daily_deturns()

    market = sd.Market(io_image=io)
    market.day_gainer_treemap()
    market.day_losers_treemap()
    market.day_most_active_treemap()

if __name__ == "__main__":
    main()
