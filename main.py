import stockplotly.stock_info as spsi
import stockplotly.basic as ba

def main():
    #stock parameter
    ticker = 'msft'
    startdate = '01/12/2020'
    enddate = '01/04/2022'
    stock = spsi.Stock(ticker, startdate, enddate)

    # stock.history_price()
    # stock.history_price_area()
    # stock.candlestick()
    # stock.Ohlc()

    market = spsi.Market()
    market.Treemap_day_gainer()
    market.Treemap_day_losers()

if __name__ == "__main__":
    main()
