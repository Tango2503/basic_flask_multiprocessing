import multiprocessing
import pandas as pd
from flask import Flask
import requests

# Multiprocessing Landing Page
    
app = Flask(__name__)
script = ""
status = ""

@app.route('/', methods=['GET', 'POST'])
def index(script):
    return script
def worker1():
    app.run(use_reloader = False)
 
def worker2(key, return_dict): 
    x = requests.get('http://127.0.0.1:5000/')
    if x.status_code == 200:
        status = "Landing Page Loaded"
    else:
        status = "Landing Page Not Loaded"  
    return_dict[key] = status

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    df_cleaned = pd.read_csv('df_cleaned.csv')
    df_cleaned = df_cleaned.iloc[0:3,:]
    codes = df_cleaned['tag_code'].to_list()
    jobs0 = jobs = []
    for i in range(len(codes)):
        script = codes[i]
        index(script)
        p0 = multiprocessing.Process(target=worker1)
        p = multiprocessing.Process(target=worker2, args=(i, return_dict))
        jobs0.append(p0)
        jobs.append(p)
        p0.start()
        p.start()
        p0.join()
        
#    for proc0 in jobs0:
#        proc0.join()
    
    for proc in jobs:
        proc.join()

        
        
    print(dict(return_dict))
    
#def worker(procnum, code, return_dict):
#    '''worker function'''
#    print(str(procnum) + ' represent!')
#    return_dict[procnum] = code[50:80]
    
#
#def landing_page_check(script_row):
#    global script, status
#    script = script_row
#    
#    # creating processes 
#    server = multiprocessing.Process(target=worker1) 
#    get_requests = multiprocessing.Process(target=worker2, args = ()) 
#    print('Here')
#    
#    
#    # starting processes 
#    server.start() 
#    get_requests.start() 
#    
#    # wait until process 2 is finished 
#    get_requests.join() 
#    
#    # Terminate the server and end the process
##    server.terminate()
#    server.join() 
#    
#    return status
#    