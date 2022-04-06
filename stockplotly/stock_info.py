from enum import Flag
from turtle import title
import yahoo_fin.stock_info as si
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as ms


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

    def candlestick(self):
        df = self.__history_price
        suffix = ' Candlestick'

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
                x=df['date'], 
                y=df['volume'], 
                showlegend=False
            ), 
            row=2, col=1
        )

        #Do not show candlestick's rangeslider plot 
        fig.update(layout_xaxis_rangeslider_visible=False)
        fig.update_layout(title_text=self.__ticker.upper()+suffix)

        fig.show()

    def Ohlc(self):
        df = self.__history_price
        suffix = ' Ohlc'

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
                x=df['date'], 
                y=df['volume'], 
                showlegend=False
            ), 
            row=2, col=1
        )

        #Do not show OHLC's rangeslider plot 
        fig.update(layout_xaxis_rangeslider_visible=False)
        fig.update_layout(title_text=self.__ticker.upper()+suffix)

        fig.show()