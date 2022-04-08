# -*- coding: utf-8 -*-

class basic():
    
    def __init__(self):
        pass

    def export(self, fig, title, status):
        if status == True:
            fig.show()
        else:
            fig.write_image("img/" + title + '.png', width=1980, height=1080)

    def as_float(self, series):
        temp = []
        for i in series:
            if type(i) != float:
                i = i.replace(".", "")
                i = float(i.replace("T", "000000000.0"))
            temp.append(i)
        return temp

    def Dateadd(date):
        temp = date.split("/")
        temp[2] = str(int(temp[2]) - 1)
        return temp[0] + '/' + temp[1] + '/' + temp[2]