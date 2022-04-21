# -*- coding: utf-8 -*-

import stockplotly.stock_draw as sd

def main():
    #stock parameter
    ticker = "tsla"
    startdate = "01/01/2020"
    enddate = "09/04/2022"
    io = True

    stock = sd.Stock(ticker, startdate, enddate, io_image=io)
    market = sd.Market(io_image=io)

    stock.history_price()
    stock.candlestick()
    stock.ohlc()
    stock.compare_area("aapl")
    stock.compare_index()
    stock.daily_deturns()
    stock.daily_deturns_volume()
    stock.company_info()

    market.day_gainer_treemap()
    market.day_losers_treemap()
    market.day_most_active_treemap()

if __name__ == "__main__":
    main()

