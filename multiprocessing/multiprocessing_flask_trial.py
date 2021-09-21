# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 13:50:32 2020

@author: tanusha.goswami
"""
import multiprocessing 
from flask import Flask, render_template
import requests
import os
import ctypes
import pandas as pd



def worker1(h,template_path):
    app = Flask(__name__, template_folder = template_path)
    @app.route('/', methods=['GET', 'POST'])
    def index():
#        print("the hstring is " + h)
        return render_template(h)
    app.run()
 
def worker2(return_dict,h): 
    x = requests.get('http://127.0.0.1:5000/')
    print(x.status_code)
    print(h)
    if x.status_code == 200:
        print('All Good')
    else:
        print('Something is up')
    return_dict[h] = x.status_code
    

        
def main():
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    
    third_party_path = 'D:/MiQ/Client Requests/Creative QA Tool/root_directory/ft_dcm_tags'
    
    df_cleaned = pd.read_csv('df_cleaned.csv')
    df_cleaned = df_cleaned.iloc[0:5,:]
    template_path = third_party_path + '/templates'
    if not os.path.exists(template_path):
        os.makedirs(template_path)
    os.chdir(template_path)
    for index, row in df_cleaned.iterrows():
        html_str = row['tag_code']           
        Html_file= open(row['html_file_name'],"w")
        Html_file.write(html_str)
        Html_file.close()
    
    os.chdir(third_party_path)
    html_path = df_cleaned['html_file_name'].to_list()
    for h in html_path:
        h_string = manager.Value(ctypes.c_char, h)
        
        # creating processes 
        p1 = multiprocessing.Process(target=worker1, args = (h_string.value,template_path)) 
        p2 = multiprocessing.Process(target=worker2, args = (return_dict,h_string.value))
        
        # starting processes 
        p1.start() 
        p2.start() 
        
        # wait until processes are finished 
        p2.join() 
        p1.terminate()
    
    third_party_status = dict(dict(return_dict))
    third_party_status = (pd.DataFrame(third_party_status, index = [0])).T
    third_party_status.columns = ['filename_placementid','status']
    htmls_loaded_incorrect = third_party_status.loc[third_party_status['status'] != 200]
    final_directory_html_incorrect = third_party_path + '/htmls_loaded_incorrect_files' + '_' + now 
    n = len(final_directory_html_incorrect)
    if n > 0: 
        message_html_incorrect = str(n) + " third party tags could not load."
        if not os.path.exists(final_directory_html_incorrect):
            os.makedirs(final_directory_html_incorrect)  
        for f1 in htmls_loaded_incorrect:
            shutil.copy(f1, final_directory_html_incorrect)
        
        
    
    print(third_party_status)

if __name__ == "__main__": 
    main()
 


