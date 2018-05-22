# user files
import source

# networking libs
import http.client
import urllib
import requests

# source
import time

# parallel programming libs
import threading as t
        
def parallel_t_requests(urls):
    threads = [t.Thread(target=fetch_url, args=(url,)) for url in urls]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()        
        
        
""" Global Variables:"""
#URL_RAW = "desolate-ravine-43301.herokuapp.com"
#conn = http.client.HTTPConnection(URL_RAW)
URL = "http://desolate-ravine-43301.herokuapp.com"    

def main_request(debug_mode):
    main_response = requests.post(URL)
    
    urls_body = main_response.json() 
    urls_header = main_response.headers        
    urls_count = len(urls_body)
    secret_key = urls_header['Session']
   
    if(debug_mode):
        source.debug_data(urls_body,urls_header)
    
    secret_key_header = { "Session" : secret_key }
    return urls_body,secret_key_header,urls_count


def refactor_urls(urls_count,urls_body,URL):
    return [(URL+urls_body[i]["path"]) for i in range(urls_count)]    
    
def fetch_url(url):
    #print("HTTP request sent!")
    try:
        s1 = time.time() 
#----------------------------
        result = requests.get(url, headers=secret_key_header)        
        process_result(result)
#----------------------------        
        e1 = time.time()
        
        print("Response time:",e1 - s1)

    
    except urllib.error.HTTPError as e:
        print("\n!!! SERVER KEY TIMED OUT!!!")
        print("Or perhaps:",e)
        e1 = time.time() #time when the failed request would've finished
        print("FAILED Response time:",e1 - s1)        
        retrying = True
    

def process_result(result):

    value_format = result.headers['Content-Type']
    device_body = source.deserialize(result,value_format)
    source.save_data(device_body, value_format)
    
    print("\nHTTP Response successful!") #debug
    #print("Device Body:",result.text)   #debug
    #print("ValueFormat: ",value_format)  #debug

"""#####################START#####################"""
retrying = True # only once   
while(retrying):
    
    """# STEP 1"""
    urls_body,secret_key_header,urls_count = main_request(True)
    """# STEP 2"""
    urls = refactor_urls(urls_count,urls_body,URL)
    """# STEP 3"""
    retrying = False #job considered complete...
    parallel_t_requests(urls)
    if(retrying): #...unless an error requests a retry
        print("\n!!! RETRYING !!!")
    
"""# STEP omega"""
source.format_and_reorder_output()