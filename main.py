import stockplotly.stock_info as spsi

def main():
    data = spsi.Stock('msft', '01/12/2019', '01/04/2022')
    data.history_price()

if __name__ == "__main__":
    main()