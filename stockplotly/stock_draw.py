# -*- coding: utf-8 -*-

from enum import Flag
from textwrap import fill
from turtle import fillcolor, title
from datetime import datetime
from unicodedata import name
from stockplotly.basic import basic
import yahoo_fin.stock_info as si
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as ms
import pandas as pd
from ta.trend import MACD 

class Stock(basic):

    def __init__(self, ticker, start_date, end_date, io_image = True):
        super().__init__(start_date, end_date)

        self.__ticker = ticker
        self.__start_date = start_date
        self.__end_date = end_date

        self.__io_image = io_image

        # No usage data
        print(("crawling " + ticker.upper() + " company finance data").ljust(50, "."), end="") 
        # self.__stats = si.get_stats(ticker)
        # self.__stats_valuation = si.get_stats_valuation(ticker)
        # self.__quote_table = si.get_quote_table(ticker, dict_result = False)
        self.__analysts_info = si.get_analysts_info(ticker)
        self.__balance_sheet = si.get_balance_sheet(ticker, yearly = True)
        self.__balance_sheet_quarterly = si.get_balance_sheet(ticker, yearly = False)
        self.__income_statement = si.get_income_statement(ticker, yearly = True)
        self.__income_statement_quarterly = si.get_income_statement(ticker, yearly = False)
        print("OK!".rjust(10,".")) 

        print(("crawling " + ticker.upper() + " history_price").ljust(50, "."), end="") 
        self.__history_price = si.get_data(
            ticker, 
            start_date=self.__start_date, 
            end_date=self.__end_date, 
            index_as_date=False,
        )
        print("OK!".rjust(10,".")) 

        # Calculate data
        print(("calculating "+ticker.upper()+" other data").ljust(50, "."), end="") 
        self.__history_price["ma10"] = self.__history_price["adjclose"].rolling(window=10).mean()
        self.__history_price["ma20"] = self.__history_price["adjclose"].rolling(window=20).mean()
        self.__history_price["ma60"] = self.__history_price["adjclose"].rolling(window=60).mean()

        self.__history_price["Daily Change %"] = super()._basic__DTD(self.__history_price["adjclose"])
        print("OK!".rjust(10,".")) 

    # methods
    def __macd(self, df, fig):

        macd = MACD(close=df['close'], window_slow=26, window_fast=12, window_sign=9)

        colors = ['green' if val >= 0 
                else 'red' for val in macd.macd_diff()]

        fig.add_trace(go.Bar(x=df.index, y=macd.macd_diff(), name="MACD histogram", marker_color=colors), row=3, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=macd.macd(), line=dict(color='red', width=1), name="DIF"), row=3, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=macd.macd_signal(), line=dict(color='blue', width=1), name="MACD"), row=3, col=1)

        return fig

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

    def compare_area(self, o_ticker):
        df = self.__history_price
        suffix = " Compare"
        title = self.__ticker.upper() + suffix + " " + o_ticker.upper() + " Area"
        super()._basic__drawstart(title)

        o_df = si.get_data(
            o_ticker, 
            start_date=self.__start_date, 
            end_date=self.__end_date, 
            index_as_date=False,
        )

        fig = px.area(title=self.__ticker.upper()+suffix)

        fig.add_trace(go.Scatter(x=df.date, y=df.adjclose, name=self.__ticker.upper(), 
        line = dict(width=1), fill='tozeroy', fillcolor="rgba(255,193,102,0.3)"))

        fig.add_trace(go.Scatter(x=o_df.date, y=o_df.adjclose, name=o_ticker.upper(), 
        line = dict(width=1), fill='tozeroy', fillcolor="rgba(168,216,185,0.3)"))

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

    def candlestick(self):
        df = self.__history_price
        suffix = " Candlestick"
        title = self.__ticker.upper()+suffix
        super()._basic__drawstart(title)
        
        fig = ms.make_subplots(
            rows=3, cols=1, 
            shared_xaxes=True, 
            vertical_spacing=0.03, 
            row_width=[0.15, 0.15, 0.7],
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

        fig = self.__macd(df, fig)

        #Do not show candlestick"s rangeslider plot 
        fig.update(layout_xaxis_rangeslider_visible=False)
        fig.update_layout(title_text=self.__ticker.upper()+suffix)

        super()._basic__export(fig, title, self.__io_image)

    def ohlc(self):
        df = self.__history_price
        suffix = " Ohlc"
        title = self.__ticker.upper()+suffix
        super()._basic__drawstart(title)

        fig = ms.make_subplots(
            rows=3, cols=1, 
            shared_xaxes=True, 
            vertical_spacing=0.03, 
            row_width=[0.15, 0.15, 0.7],
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

        fig = self.__macd(df, fig)

        #Do not show OHLC"s rangeslider plot 
        fig.update(layout_xaxis_rangeslider_visible=False)
        fig.update_layout(title_text=self.__ticker.upper()+suffix)

        super()._basic__export(fig, title, self.__io_image)

    def compare_index(self):
        df = self.__history_price
        suffix = " Compare index"
        title = self.__ticker.upper() + suffix

        dji = self._basic__DJI
        sp500 = self._basic__GSPC
        nasdaq = self._basic__IXIC
        ru2000 = self._basic__RUT

        dji["Daily Change %"] = super()._basic__DTD(dji["adjclose"])
        sp500["Daily Change %"] = super()._basic__DTD(sp500["adjclose"])
        nasdaq["Daily Change %"] = super()._basic__DTD(nasdaq["adjclose"])
        ru2000["Daily Change %"] = super()._basic__DTD(ru2000["adjclose"])

        super()._basic__drawstart(title)

        fig = px.line(title=self.__ticker.upper()+suffix)
        fig.add_trace(go.Scatter(x=df["date"], y=df["Daily Change %"],name=self.__ticker, 
            line = dict(width=2, color='red')))

        fig.add_trace(go.Scatter(x=dji["date"], y=dji["Daily Change %"],name="DJI", 
            line = dict(width=1, color='royalblue')))
        fig.add_trace(go.Scatter(x=sp500["date"], y=sp500["Daily Change %"],name="S&P500", 
            line = dict(width=1, color='green')))
        fig.add_trace(go.Scatter(x=nasdaq["date"], y=nasdaq["Daily Change %"],name="NASDAQ", 
            line = dict(width=1, color='yellow')))
        fig.add_trace(go.Scatter(x=ru2000["date"], y=ru2000["Daily Change %"],name="Russell 2000", 
            line = dict(width=1, color='orange')))

        super()._basic__export(fig, title, self.__io_image)

    def daily_deturns(self):
        df = self.__history_price
        df['Daily Return %'] = (df['close']/df['close'].shift(1)) -1
        suffix = " Daily Returns"
        title = self.__ticker.upper()+suffix
        super()._basic__drawstart(title)

        fig = px.histogram(df, x="Daily Return %", marginal="box", histnorm='percent', nbins=80, title=self.__ticker.upper()+suffix)

        fig.add_vline(x=df['Daily Return %'].mean(), line_width=1, line_dash="dashdot", line_color="red")

        super()._basic__export(fig, title, self.__io_image)

    def daily_deturns_volume(self):
        df = self.__history_price
        df['Daily Return %'] = (df['close']/df['close'].shift(1)) -1
        suffix = " Daily Returns volume"
        title = self.__ticker.upper()+suffix
        super()._basic__drawstart(title)

        fig = px.scatter(x=df["Daily Return %"], y=df["volume"], color=df["volume"], trendline="ols", title=self.__ticker.upper()+suffix)

        super()._basic__export(fig, title, self.__io_image)

    def company_info(self):
        # Total Revenue
        ins = self.__income_statement.T
        ins_q = self.__income_statement_quarterly.T

        # Balance Sheet
        sheet = self.__balance_sheet
        cash = sheet.loc["cash"]
        tcl = sheet.loc["totalCurrentLiabilities"]

        sheet_q = self.__balance_sheet_quarterly
        cash_q = sheet_q.loc["cash"]
        tcl_q = sheet_q.loc["totalCurrentLiabilities"]

        # Earnings History
        ai_eh = self.__analysts_info["Earnings History"]
        ai_eh = ai_eh.set_index("Earnings History")
        ai_eh = ai_eh.T

        # Growth Estimates
        ai_ge = self.__analysts_info["Growth Estimates"]
        ai_ge = ai_ge.set_index("Growth Estimates")

        # Title
        suffix = " Company information"
        title = self.__ticker.upper()+suffix
        super()._basic__drawstart(title)

        fig = ms.make_subplots(
            rows=2, cols=3, 
            shared_xaxes=False, 
            vertical_spacing=0.08, 
            subplot_titles=("totalRevenue Year","totalRevenue Quarterly", "EPS", 
                "Cash flow Year", "Cash flow Quarterly", "EPS Growth Estimates")
        )

        fig.add_trace(go.Bar(x=ins.index, y=ins.totalRevenue, name="TR Year", 
            marker=dict(color='cornflowerblue')), row=1, col=1)
        fig.add_trace(go.Bar(x=ins.index, y=ins.costOfRevenue, name="CR Year", 
            marker=dict(color='salmon')), row=1, col=1)

        fig.add_trace(go.Bar(x=ins_q.index, y=ins_q.totalRevenue, name="TR Quarterly", 
            marker=dict(color='royalblue')), row=1, col=2)
        fig.add_trace(go.Bar(x=ins_q.index, y=ins_q.costOfRevenue, name="CR Quarterly", 
            marker=dict(color='firebrick')), row=1, col=2)

        fig.add_trace(go.Bar(x=ai_eh.index, y=ai_eh["EPS Est."], name="EPS Est.", 
            marker=dict(color='lightgreen')), row=1, col=3)
        fig.add_trace(go.Bar(x=ai_eh.index, y=ai_eh["EPS Actual"], name="EPS Actual", 
            marker=dict(color="green")), row=1, col=3)

        fig.add_trace(go.Bar(x=list(sheet), y=cash, name="Cash Year", 
            marker=dict(color='cornflowerblue')), row=2, col=1)
        fig.add_trace(go.Bar(x=list(sheet), y=tcl, name="tCL Year", 
            marker=dict(color='salmon')), row=2, col=1)

        fig.add_trace(go.Bar(x=list(sheet_q), y=cash_q, name="Cash Quarterly", 
            marker=dict(color='royalblue')), row=2, col=2)
        fig.add_trace(go.Bar(x=list(sheet_q), y=tcl_q, name="tCL Quarterly", 
            marker=dict(color='firebrick')), row=2, col=2)

        fig.add_trace(go.Bar(x=ai_ge.index, y=ai_ge[self.__ticker.upper()], name="EPS Est.", 
            marker=dict(color='steelblue')), row=2, col=3)

        fig.update_layout(title_text=title)

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