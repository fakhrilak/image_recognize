filtered = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

def filter(input):
    tampung = ""
    for k in input:
        for i in filtered:
            if i == k:
                tampung+=i
    return tampung

def number_analys(index,str):
    data = str
    statement = len(data[index[0]:index[len(index)-1]+1])
    if statement > 4:
        for i in index[::-1]:
            print(data[index[0]:i+1],i)
            ## return number index of
            return i
    # while len(data[index[0]:index[len(index)-1]+1]) > 4:
        
    # for i in index[::-1]:
    #     print(data[index[0]:i+1])

def analys():
    data = "B1190P1E"
    index = []
    for count,i in enumerate(data):
        try:
            a = int(i)
            index.append(count)
        except BaseException as err:
            print(err)
    # print(data[:index[0]],data[index[0]:index[len(index)-1]+1],data[index[len(index)-1]+1:])
    # for i in index[::-1]:
    #     print(data[index[0]:i+1])
    number_index = number_analys(index,data)
    return {
        "daerah": data[:index[0]],
        "number_plate" : data[index[0]:number_index-1],
        "sub_daerah" : data[index[len(index)-1]+1:]
    }
print(analys())