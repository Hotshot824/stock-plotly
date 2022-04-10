# -*- coding: utf-8 -*-
import yahoo_fin.stock_info as si

class basic():
    
    def __init__(self, start_date, end_date):
        # DJI index

        print("crawling Dow Jones index data".ljust(50, "."), end="") 
        self.__DJI = si.get_data(
            "^DJI", 
            start_date=start_date, 
            end_date=end_date, 
            index_as_date=False,
        )
        print("OK!".rjust(10,".")) 

        # Nasdaq index
        print("crawling Nasdaq index data".ljust(50, "."), end="") 
        self.__IXIC = si.get_data( 
            "^IXIC", 
            start_date=start_date, 
            end_date=end_date, 
            index_as_date=False,
        )
        print("OK!".rjust(10,".")) 

        # S&P500 index
        print("crawling S&P500 index data".ljust(50, "."), end="") 
        self.__GSPC = si.get_data(
            "^GSPC", 
            start_date=start_date, 
            end_date=end_date, 
            index_as_date=False,
        )
        print("OK!".rjust(10,".")) 

        # Russell 2000 index
        print("crawling Russell 2000 index data".ljust(50, "."), end="") 
        self.__RUT = si.get_data(
            "^RUT", 
            start_date=start_date, 
            end_date=end_date, 
            index_as_date=False,
        )
        print("OK!".rjust(10,".")) 

    # methods
    def __drawstart(self, title):
        print(("drawing " + title).ljust(50, "."), end="") 

    def __export(self, fig, title, io_image):
        if io_image == True:
            fig.write_image("img/" + title + '.jpg', width=1980, height=1080)
        else:
            fig.show()
        print("OK!".rjust(10,".")) 

    def __as_float(self, series):
        temp = []
        for i in series:
            if type(i) != float:
                i = i.replace(".", "")
                i = float(i.replace("T", "000000000.0"))
            temp.append(i)
        return temp

    def __DTD(self, series):
        temp = []
        start = series.iat[0]
        for i in series:
            temp.append(i / start)
        return temp

    def __Dateadd(date):
        temp = date.split("/")
        temp[2] = str(int(temp[2]) - 1)
        return temp[0] + '/' + temp[1] + '/' + temp[2]