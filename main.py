# -*- coding: utf-8 -*-

import stockplotly.stock_draw as sd

def main():
    #stock parameter
    ticker = 'tsla'
    startdate = '01/12/2020'
    enddate = '01/04/2022'

    stock = sd.Stock(ticker, startdate, enddate, io_image=True)
    stock.history_price()
    stock.history_price_area()
    stock.candlestick()
    stock.Ohlc()
    stock.history_price_pc()

    market = sd.Market(io_image=True)
    market.day_gainer_treemap()
    market.day_losers_treemap()
    market.day_most_active_treemap()

if __name__ == "__main__":
    main()
