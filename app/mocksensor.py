import requests

for i in range(50):
    date = "2019/1/22 17:02:" + int(i)
    temp = i // 2
    hum = i

    res = requests.get("http://localhost:5000/addrecord/?temp="+int(temp)+"&hum="+int(hum))


