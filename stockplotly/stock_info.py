from enum import Flag
from turtle import title
import yahoo_fin.stock_info as si
import plotly.express as px
import plotly.graph_objects as go


class Stock():

    def __init__(self, ticker, start_date, end_date):
        self.__ticker = ticker
        self.__start_date = start_date
        self.__end_date = end_date

        self.__history_price = si.get_data(
            ticker, 
            start_date=self.__start_date, 
            end_date=self.__end_date, 
            index_as_date=False,
        )

        self.__history_price["ma10"] = self.__history_price["adjclose"].rolling(10).mean()
        self.__history_price["ma20"] = self.__history_price["adjclose"].rolling(20).mean()
        self.__history_price["ma60"] = self.__history_price["adjclose"].rolling(60).mean()

    def history_price(self):
        df = self.__history_price
        suffix = ' History Price'

        fig = px.line(df, x="date", y='adjclose', title=self.__ticker.upper()+suffix)
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

        fig.show()

    def candlestick(self):
        df = self.__history_price
        suffix = ' Candlestick'
        fig = go.Figure(
            data = [go.Candlestick(
                x = df.date,
                open = df.open,
                high = df.high,
                low = df.low,
                close = df.close,
                increasing_line_color = 'red',
                decreasing_line_color = 'green'
            )],
            layout = go.Layout(title=go.layout.Title(text=self.__ticker.upper()+suffix))
        )

        fig.add_trace(go.Scatter(x=df.date, y=df.ma10,name="Ma10", line = dict(width=1)))
        fig.add_trace(go.Scatter(x=df.date, y=df.ma20,name="Ma20", line = dict(width=1)))
        fig.add_trace(go.Scatter(x=df.date, y=df.ma60,name="Ma60", line = dict(width=1)))

        fig.show()

    def Ohlc(self):
        df = self.__history_price
        suffix = ' Ohlc'
        fig = go.Figure(
            data = [go.Ohlc(
                x = df.date,
                open = df.open,
                high = df.high,
                low = df.low,
                close = df.close,
            )],
            layout = go.Layout(title=go.layout.Title(text=self.__ticker.upper()+suffix))
        )

        fig.add_trace(go.Scatter(x=df.date, y=df.ma10,name="Ma10", line = dict(width=1)))
        fig.add_trace(go.Scatter(x=df.date, y=df.ma20,name="Ma20", line = dict(width=1)))
        fig.add_trace(go.Scatter(x=df.date, y=df.ma60,name="Ma60", line = dict(width=1)))

        fig.show()

    def history_price_area(self):
        df = self.__history_price
        suffix = ' Price Area'
        fig = px.area(x=df.date, y=df.adjclose, title=self.__ticker.upper()+suffix)

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

        fig.show()