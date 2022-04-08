# -*- coding: utf-8 -*-

class basic():
    
    def __init__(self):
        pass

    def __export(self, fig, title, io_image):
        if io_image == True:
            fig.write_image("img/" + title + '.jpg', width=1980, height=1080)
        else:
            fig.show()

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