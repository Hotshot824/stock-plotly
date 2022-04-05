import stockplotly.stock_info as spsi

def main():
    ticker = 'msft'
    startdate = '01/12/2019'
    enddate = '01/04/2022'
    stock = spsi.Stock(ticker, startdate, enddate)
    # stock.history_price()
    stock.candlestick()

if __name__ == "__main__":
    main()