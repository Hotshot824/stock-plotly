
def Dateadd(date):
    temp = date.split("/")
    temp[2] = str(int(temp[2]) - 1)
    return temp[0] + '/' + temp[1] + '/' + temp[2]

def as_float(series):
    temp = []
    for i in series:
        if type(i) != float:
            i = i.replace(".", "")
            i = float(i.replace("T", "000000000.0"))
        temp.append(i)
    return temp