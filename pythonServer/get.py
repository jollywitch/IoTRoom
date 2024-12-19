import requests
import json

SERVER = "localhost"
PORT = 7579

headers = {"Accept" : "application/json",
           "X-M2M-RI" : "12345",
           "X-M2M-Origin" : "S"}

sensorNameList = ["temp", "humi", "heat_index", "lumi"]
requestDataList = []
dataDict = {}

def fetchLatestData():
    for i in sensorNameList:
        requestDataList.append(requests.get("http://%s:%s/Mobius/sensor/%s/latest" % (SERVER, PORT, i), headers=headers).text)

    jsonList = [json.loads(string) for string in requestDataList]

    for i in range(len(sensorNameList)):
        dataDict[sensorNameList[i]] = jsonList[i]["m2m:cin"]["con"]["v"]

    return dataDict

if __name__ == "__main__":
    print(fetchLatestData())
