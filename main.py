import stockplotly.stock_info as spsi
import stockplotly.basic as ba

def main():
    #stock parameter
    ticker = 'tsla'
    startdate = '01/12/2020'
    enddate = '01/04/2022'
    stock = spsi.Stock(ticker, startdate, enddate, io_status=False)

    stock.history_price()
    stock.history_price_area()
    stock.candlestick()
    stock.Ohlc()

    market = spsi.Market(io_status=False)
    market.Treemap_day_gainer()
    market.Treemap_day_losers()
    market.Treemap_day_most_active()

if __name__ == "__main__":
    main()
