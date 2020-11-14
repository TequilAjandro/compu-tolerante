def sqlnRect(lng,wdth,res = []):
    if lng == wdth:
        res.append(lng)
        return res
    elif lng < wdth:
        res.append(lng)
        wdth=wdth-lng
        return sqlnRect(lng,wdth,res)
    elif wdth < lng:
        res.append(wdth)
        lng=lng-wdth
        return sqlnRect(lng,wdth,res)

while True:
    lng = int(input("ingrese longitud\n"))
    wdth = int(input("ingrese altura\n"))
    print (sqlnRect(lng,wdth))