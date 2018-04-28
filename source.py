import requests
from threading import Thread
import xml.etree.ElementTree
import unicodedata
# Devices
Device0="Temperature"
Device1="Humidity"
Device2="Motion"
Device3="Alien Presence"
Device4="Dark Matter"
Device5="T.Secret"

# Server
URL = "https://desolate-ravine-43301.herokuapp.com/"
ListOfDevices = []

ListOfUrls = []
Secret_key = {}

threads = []

url_list_count = 0
parsed_urls = 0

def get_key():

    global url_list_count
    
    r = requests.post(URL)

    jsonBody = r.json()

    headers = r.headers
    secret_key = headers['Session']
    Secret_key = {"Session" : secret_key}

    for urlItem in jsonBody:
        
        ListOfUrls.append(urlItem)

    url_list_count = len(ListOfUrls)

    return Secret_key

def get_data(url):

    global parsed_urls, url_list_count

    if(url['method'] == 'GET'):
        r = requests.get(URL + url['path'], headers=Secret_key)
    else:
        r = requests.post(URL + url['path'], headers=Secret_key)

    response_format = r.headers['Content-Type']

    if(response_format == "Application/xml"):
        e = xml.etree.ElementTree.fromstring(r.text)

        tempObj = {"id" : e.attrib['id']}

        for child in e:
            if(child.tag == "type"):
                tempObj['type'] = child.text
            else:
                tempObj['value'] = child.text

        ListOfDevices.append(tempObj)

    elif(response_format == "Application/json"):
        
        json_response = r.json()

        tempObj = {"id": json_response["device_id"], "type": json_response["sensor_type"], "value": json_response["value"]}

        ListOfDevices.append(tempObj)

    else:
        response_text = r.text
        splitted_text = response_text.split("\n")

        for i in range(len(splitted_text)):
            if i != 0:
                split_new_text = splitted_text[i].split(",")

                if len(split_new_text) == 3:

                    device_id = unicodedata.normalize('NFKD', split_new_text[0]).encode('ascii', 'ignore')
                    devide_type = unicodedata.normalize('NFKD', split_new_text[1]).encode('ascii', 'ignore')
                    device_value = unicodedata.normalize('NFKD', split_new_text[2]).encode('ascii', 'ignore')

                    tempObj = {"id": device_id, "type": int(devide_type), "value": float(device_value)}

                    ListOfDevices.append(tempObj)
    
    parsed_urls = parsed_urls + 1

    if(parsed_urls == url_list_count):
        show_result()
    

def show_result():
    for i in range(6):
        if(i == 0):
            print()
            dName = Device0
            print(dName)
            for device in ListOfDevices:
                if(device['type'] == i):
                    print('Device ' + str(device['id']) + ' - ' + str(device['value']))
        elif(i == 1):
            print()
            dName = Device1
            print(dName)
            for device in ListOfDevices:
                if(device['type'] == i):
                    print('Device ' + str(device['id']) + ' - ' + str(device['value']))
        elif(i == 2):
            print()
            dName = Device2
            print(dName)
            for device in ListOfDevices:
                if(device['type'] == i):
                    print('Device ' + str(device['id']) + ' - ' + str(device['value']))
        elif(i == 3):
            print()
            dName = Device3
            print(dName)
            for device in ListOfDevices:
                if(device['type'] == i):
                    print('Device ' + str(device['id']) + ' - ' + str(device['value']))
        elif(i == 4):
            print()
            dName = Device4
            print(dName)
            for device in ListOfDevices:
                if(device['type'] == i):
                    print('Device ' + str(device['id']) + ' - ' + str(device['value']))
        else:
            dName = Device5
            print(dName)
            for device in ListOfDevices:
                if(device['type'] == i):
                    print('Device ' + str(device['id']) + ' - ' + str(device['value']))
        print()



def get_parallel_requests():
    for url in ListOfUrls:
        threads = []
        threads.append(Thread(target=get_data, args=(url,)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

Secret_key = get_key()
get_parallel_requests()
