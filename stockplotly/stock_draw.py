# -*- coding: utf-8 -*-

from enum import Flag
from turtle import title
from datetime import datetime
from stockplotly.basic import basic
import yahoo_fin.stock_info as si
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as ms
import pandas as pd

class Stock(basic):

    def __init__(self, ticker, start_date, end_date, io_image = True):
        super().__init__(start_date, end_date)

        self.__ticker = ticker
        self.__start_date = start_date
        self.__end_date = end_date

        self.__io_image = io_image

        # No usage data
        print(("Crawling " + ticker.upper() + " get_stats").ljust(50, "."), end="") 
        self.__stats = si.get_stats(ticker)
        print("OK!".rjust(10,".")) 

        print(("Crawling " + ticker.upper() + " stats_valuation").ljust(50, "."), end="") 
        self.__stats_valuation = si.get_stats_valuation(ticker)
        print("OK!".rjust(10,".")) 

        print(("Crawling " + ticker.upper() + " quote_table").ljust(50, "."), end="") 
        self.__quote_table = si.get_quote_table(ticker, dict_result = False)
        print("OK!".rjust(10,".")) 

        print(("Crawling " + ticker.upper() + " history_price").ljust(50, "."), end="") 
        self.__history_price = si.get_data(
            ticker, 
            start_date=self.__start_date, 
            end_date=self.__end_date, 
            index_as_date=False,
        )
        print("OK!".rjust(10,".")) 

        # Calculate data
        print(("Calculating "+ticker.upper()+" other data").ljust(50, "."), end="") 
        self.__history_price["ma10"] = self.__history_price["adjclose"].rolling(10).mean()
        self.__history_price["ma20"] = self.__history_price["adjclose"].rolling(20).mean()
        self.__history_price["ma60"] = self.__history_price["adjclose"].rolling(60).mean()

        self.__history_price["Daily Change %"] = super()._basic__DTD(self.__history_price["adjclose"])
        print("OK!".rjust(10,".")) 

    # methods
    def history_price(self):
        df = self.__history_price
        suffix = " History Price"
        title = self.__ticker.upper()+suffix
        super()._basic__drawstart(title)

        fig = px.line(df, x="date", y="adjclose", title=title)
        fig.add_trace(go.Scatter(x=df.date, y=df.ma10,name="Ma10", line = dict(width=1)))
        fig.add_trace(go.Scatter(x=df.date, y=df.ma20,name="Ma20", line = dict(width=1)))
        fig.add_trace(go.Scatter(x=df.date, y=df.ma60,name="Ma60", line = dict(width=1)))

        fig.update_xaxes(
            rangeslider_visible=True,   
            rangeselector=dict(
                buttons=list([
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )

        super()._basic__export(fig, title, self.__io_image)

    def history_price_area(self):
        df = self.__history_price
        suffix = " History Price Area"
        title = self.__ticker.upper()+suffix
        super()._basic__drawstart(title)

        fig = px.area(df, x="date", y="adjclose", title=self.__ticker.upper()+suffix)

        fig.update_xaxes(
            rangeslider_visible=True,   
            rangeselector=dict(
                buttons=list([
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )

        super()._basic__export(fig, title, self.__io_image)

    def history_price_ROI(self):
        df = self.__history_price
        suffix = " Return on Investment"
        title = self.__ticker.upper()+suffix

        dji = self._basic__DJI
        sp500 = self._basic__GSPC
        nasdaq = self._basic__IXIC

        dji["Daily Change %"] = super()._basic__DTD(dji["adjclose"])
        sp500["Daily Change %"] = super()._basic__DTD(sp500["adjclose"])
        nasdaq["Daily Change %"] = super()._basic__DTD(nasdaq["adjclose"])

        super()._basic__drawstart(title)

        fig = px.line(df, x="date", y="Daily Change %", title=self.__ticker.upper()+suffix)
        fig.update_traces(line_color='red', line_width=2)

        fig.add_trace(go.Scatter(x=dji["date"], y=dji["Daily Change %"],name="DJI", 
            line = dict(width=2, color='royalblue')))
        fig.add_trace(go.Scatter(x=sp500["date"], y=sp500["Daily Change %"],name="S&P500", 
            line = dict(width=2, color='green')))
        fig.add_trace(go.Scatter(x=nasdaq["date"], y=nasdaq["Daily Change %"],name="NASDAQ", 
            line = dict(width=2, color='yellow')))

        super()._basic__export(fig, title, self.__io_image)


    def candlestick(self):
        df = self.__history_price
        suffix = " Candlestick"
        title = self.__ticker.upper()+suffix
        super()._basic__drawstart(title)
        
        fig = ms.make_subplots(
            rows=2, cols=1, 
            shared_xaxes=True, 
            vertical_spacing=0.03, 
            row_width=[0.2, 0.8],
        )

        #Plot candlestick on 1st row
        fig.add_trace(
            go.Candlestick(
                x=df["date"], 
                open=df["open"], 
                high=df["high"],
                low=df["low"],
                close=df["close"], 
                name="Candlestick"
            ), 
            row=1, col=1
        )

        fig.add_trace(go.Scatter(x=df.date, y=df.ma10,name="Ma10", line = dict(width=1)))
        fig.add_trace(go.Scatter(x=df.date, y=df.ma20,name="Ma20", line = dict(width=1)))
        fig.add_trace(go.Scatter(x=df.date, y=df.ma60,name="Ma60", line = dict(width=1)))

        #Bar trace for volumes on 2nd row without legend
        fig.add_trace(
            go.Bar(
                x=df["date"], 
                y=df["volume"], 
                showlegend=False
            ), 
            row=2, col=1
        )

        #Do not show candlestick"s rangeslider plot 
        fig.update(layout_xaxis_rangeslider_visible=False)
        fig.update_layout(title_text=self.__ticker.upper()+suffix)

        super()._basic__export(fig, title, self.__io_image)

    def Ohlc(self):
        df = self.__history_price
        suffix = " Ohlc"
        title = self.__ticker.upper()+suffix
        super()._basic__drawstart(title)

        fig = ms.make_subplots(
            rows=2, cols=1, 
            shared_xaxes=True, 
            vertical_spacing=0.03, 
            row_width=[0.2, 0.8],
        )

        #Plot Ohlc on 1st row
        fig.add_trace(
            go.Ohlc(
                x=df["date"], 
                open=df["open"], 
                high=df["high"],
                low=df["low"],
                close=df["close"], 
                name="OHLC"
            ), 
            row=1, col=1
        )

        fig.add_trace(go.Scatter(x=df.date, y=df.ma10,name="Ma10", line = dict(width=1)))
        fig.add_trace(go.Scatter(x=df.date, y=df.ma20,name="Ma20", line = dict(width=1)))
        fig.add_trace(go.Scatter(x=df.date, y=df.ma60,name="Ma60", line = dict(width=1)))

        #Bar trace for volumes on 2nd row without legend
        fig.add_trace(
            go.Bar(
                x=df["date"], 
                y=df["volume"], 
                showlegend=False
            ), 
            row=2, col=1
        )

        #Do not show OHLC"s rangeslider plot 
        fig.update(layout_xaxis_rangeslider_visible=False)
        fig.update_layout(title_text=self.__ticker.upper()+suffix)

        super()._basic__export(fig, title, self.__io_image)

    def percentage_increase(self):
        df = self.__history_price
        df['Percentage'] = (df['close']/df['close'].shift(1)) -1
        suffix = " Percentage Increase"
        title = self.__ticker.upper()+suffix
        super()._basic__drawstart(title)

        fig = px.histogram(df, x="Percentage", title=self.__ticker.upper()+suffix)

        super()._basic__export(fig, title, self.__io_image)

class Market(basic):

    def __init__(self, io_image = True):
        self.__day_gainers = si.get_day_gainers()
        self.__day_losers = si.get_day_losers()
        self.__day_most_active = si.get_day_most_active()

        self.__io_image = io_image

    def day_gainer_treemap(self):
        df = self.__day_gainers
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        suffix = " Day gainer"
        title = date+suffix
        super()._basic__drawstart(title)

        df["Market Cap"] = super()._basic__as_float(df["Market Cap"])

        fig = px.treemap(
            df, path=[px.Constant("Market Cap"),"Symbol", "% Change"], values="Market Cap",
            color="Market Cap", color_continuous_scale="Portland",
            title=title)
        
        super()._basic__export(fig, suffix[1:], self.__io_image)

    def day_losers_treemap(self):
        df = self.__day_losers
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        suffix = " Day losers"
        title = date+suffix
        super()._basic__drawstart(title)

        df["Market Cap"] = super()._basic__as_float(df["Market Cap"])

        fig = px.treemap(
            df, path=[px.Constant("Market Cap"),"Symbol", "% Change"], values="Market Cap",
            color="Market Cap", color_continuous_scale="RdBu",
            title=title)
        
        super()._basic__export(fig, suffix[1:], self.__io_image)

    def day_most_active_treemap(self):
        df = self.__day_most_active
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        suffix = " Day most active"
        title = date+suffix
        super()._basic__drawstart(title)
        
        df["Market Cap"] = super()._basic__as_float(df["Market Cap"])

        fig = px.treemap(
            df, path=[px.Constant("Market Cap"), "Symbol", "% Change"], values="Market Cap",
            color="Market Cap", color_continuous_scale="YlGn",
            title=title)
        
        super()._basic__export(fig, suffix[1:], self.__io_image)