
def Dateadd(date):
    temp = date.split("/")
    temp[2] = str(int(temp[2]) - 1)
    return temp[0] + '/' + temp[1] + '/' + temp[2]