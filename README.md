# stock-plotly

## Introduction

This API based on yahoo_fin and plotly, able to do simple stock analysis diagram.

## Requires python package
```
pip install yahoo_fin == 0.8.9.1

pip install plotly == 5.6.0

pip install -U kaleido==0.2.1

# ts is a technical analysis library
pip install ta == 0.9.0
```

# Methods

```
    # Stock class methods
    stock = sd.Stock(ticker, startdate, enddate, io_image=True)

    stock.history_price()

    stock.candlestick()

    stock.ohlc()
    
    stock.compare_area("aapl")

    stock.compare_index()

    stock.daily_deturns()

    stock.daily_deturns_volume()

    stock.company_info()

    # Marker class methods
    market = sd.Market(io_image=io)

    market.day_gainer_treemap()

    market.day_losers_treemap()

    market.day_most_active_treemap()
```

# Stock Class

## history price
![](https://github.com/Hotshot824/stock-plotly/blob/main/img/TSLA%20History%20Price.jpg?raw=true)

## candlestick
![](https://github.com/Hotshot824/stock-plotly/blob/main/img/TSLA%20Candlestick.jpg?raw=true)

## ohlc
![](https://github.com/Hotshot824/stock-plotly/blob/main/img/TSLA%20Ohlc.jpg?raw=true)

## compare index
![](https://github.com/Hotshot824/stock-plotly/blob/main/img/TSLA%20Compare%20index.jpg?raw=true)

## compart stock price

![](https://github.com/Hotshot824/stock-plotly/blob/main/img/TSLA%20Compare%20AAPL.jpg?raw=true)

## company infomation

![](https://github.com/Hotshot824/stock-plotly/blob/main/img/TSLA%20Company%20information.jpg?raw=true)

## daily returns

![](https://github.com/Hotshot824/stock-plotly/blob/main/img/TSLA%20Daily%20Returns.jpg?raw=true)

## daily return volume

![](https://github.com/Hotshot824/stock-plotly/blob/main/img/TSLA%20Daily%20Returns%20volume.jpg?raw=true)


# Market Class

## Treemap 

- [x] Treemap base is market Cap (Intraday)

![](https://github.com/Hotshot824/stock-plotly/blob/main/img/Day%20gainer.jpg?raw=true)

![](https://github.com/Hotshot824/stock-plotly/blob/main/img/Day%20losers.jpg?raw=true)

![](https://github.com/Hotshot824/stock-plotly/blob/main/img/Day%20most%20active.jpg?raw=true)