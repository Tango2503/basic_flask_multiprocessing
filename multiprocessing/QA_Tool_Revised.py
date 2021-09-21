import pandas as pd
import os
from os import path
import requests
import shutil
from tkinter import filedialog, scrolledtext, Menu, messagebox, HORIZONTAL
import tkinter as tk
from tkinter.ttk import Progressbar
import glob
import re
from datetime import datetime 
from PIL import Image
import multiprocessing 
from flask import Flask, render_template
import ctypes
from math import floor

""" 
RUNNING IN CMD PROMPT :
    1. cd /d D:\MiQ\Client Requests\Creative QA Tool
    2. python QA_Tool_Revised.py
    
"""

""" 
STILL TO SOLVE :
    1. Check show_message function if no errors were present. (Works)
    2. What if sub directory doesn't exist? (Exception case to skip such a scenario) (Works)
    3. Third party - window keeps closing for each loop (Done)
    4. Convert to exe file
    5. Check for more cases
    
"""


def help_faqs():
    tk.messagebox.showinfo('FAQs', 'This is a tool built in Python')
    
def help_contactus():
    tk.messagebox.showinfo('Contact Us', 'This is a tool built in Python')

def show_message(message_file_check, message_size_check, message_gift_non_static):
    if len(message_file_check + message_size_check) == 0:
        message = "Raw Assets are good to go!"
    else:
        message = message_file_check + "\n" + message_size_check + "\n" + message_gift_non_static + "\nPlease check the root directory for incorrect files."
    
    window1 = tk.Toplevel()
    window1.wm_withdraw()
    messagebox.showinfo(title="Raw Assets Status", message = message)
    window1.destroy()
    
'''                 HTML STATUS CODES               '''

html_status_codes = {'100':['Information Response','Continue','This interim response indicates that everything so far is OK and that the client should continue the request, or ignore the response if the request is already finished'],
                     '101':['Information Response','Switching Protocol', 'This code is sent in response to an Upgrade request header from the client, and indicates the protocol the server is switching to.'],
                     '103':['Information Response','Early Hints','This status code is primarily intended to be used with the Link header, letting the user agent start preloading resources while the server prepares a response.'],
                     '200':['Successful responses','OK', 'The request has succeeded.'],
                     '201':['Successful responses','Created', 'The request has succeeded and a new resource has been created as a result.'],
                     '202':['Successful responses','Accepted', 'The request has been received but not yet acted upon.'],
                     '203':['Successful responses','Non-Authorative Information','This response code means the returned meta-information is not exactly the same as is available from the origin server, but is collected from a local or a third-party copy.'],
                     '204':['Successful responses','No Content', 'There is no content to send for this request, but the headers may be useful'],
                     '205':['Successful responses','Reset Content', 'Tells the user-agent to reset the document which sent this request.'],
                     '206':['Successful responses','Partial Content', 'This response code is used when the Range header is sent from the client to request only part of a resource.'],
                     '300':['Redirection messages','Multiple Choice', 'The request has more than one possible response. The user-agent or user should choose one of them.'],
                     '301':['Redirection messages','Moved Permanently', 'The URL of the requested resource has been changed permanently. The new URL is given in the response.'],
                     '302':['Redirection messages','Found', 'This response code means that the URI of requested resource has been changed temporarily. Further changes in the URI might be made in the future. Therefore, this same URI should be used by the client in future requests.'],
                     '303':['Redirection messages','See Other','The server sent this response to direct the client to get the requested resource at another URI with a GET request.'],
                     '304':['Redirection messages','Not Modified','This is used for caching purposes. It tells the client that the response has not been modified, so the client can continue to use the same cached version of the response.'],
                     '307':['Redirection messages','Temporary Redirect','The server sends this response to direct the client to get the requested resource at another URI with same method that was used in the prior request.'],
                     '308':['Redirection messages','Permanent Redirect','This means that the resource is now permanently located at another URI, specified by the Location: HTTP Response header.'],
                     '400':['Client error responses','Bad Request','The server could not understand the request due to invalid syntax.'],
                     '401':['Client error responses','Unauthorised','Although the HTTP standard specifies "unauthorized", semantically this response means "unauthenticated". That is, the client must authenticate itself to get the requested response.'],
                     '402':['Client error responses','Payment Required','This response code is reserved for future use. The initial aim for creating this code was using it for digital payment systems, however this status code is used very rarely and no standard convention exists.'],
                     '403': ['Client error responses',"Forbidden","The client does not have access rights to the content; that is, it is unauthorized, so the server is refusing to give the requested resource. Unlike 401, the client's identity is known to the server."],
                     '404': ['Client error responses','Not Found','The server can not find the requested resource. In the browser, this means the URL is not recognized.'],
                     '405': ['Client error responses','Method Not Allowed','The request method is known by the server but has been disabled and cannot be used. '],
                     '406': ['Client error responses','Not Acceptable',"This response is sent when the web server, after performing server-driven content negotiation, doesn't find any content that conforms to the criteria given by the user agent."],
                     '407': ['Client error responses','Proxy Authentication Required','This is similar to 401 but authentication is needed to be done by a proxy.'],
                     '408': ['Client error responses','Request Timeout','This response is sent on an idle connection by some servers, even without any previous request by the client. It means that the server would like to shut down this unused connection. '],
                     '409': ['Client error responses','Conflict','This response is sent when a request conflicts with the current state of the server.'],
                     '410': ['Client error responses','Gone','This response is sent when the requested content has been permanently deleted from server, with no forwarding address. Clients are expected to remove their caches and links to the resource. '],
                     '411': ['Client error responses','Length Required','Server rejected the request because the Content-Length header field is not defined and the server requires it.'],
                     '412': ['Client error responses','Precondition Failed','The client has indicated preconditions in its headers which the server does not meet.'],
                     '413': ['Client error responses','Payload Too Large','Request entity is larger than limits defined by server; the server might close the connection or return an Retry-After header field.'],
                     '414': ['Client error responses','URI Too Long','The URI requested by the client is longer than the server is willing to interpret.'],
                     '415': ['Client error responses','Unsupported Media Type','The media format of the requested data is not supported by the server, so the server is rejecting the request.'],
                     '416': ['Client error responses',"Range Not Satisfiable","The range specified by the Range header field in the request can't be fulfilled; it's possible that the range is outside the size of the target URI's data."],
                     '417': ['Client error responses','Expectation Failed',"This response code means the expectation indicated by the Expect request header field can't be met by the server."],
                     '418': ['Client error responses',"I'm a teapot",'The server refuses the attempt to brew coffee with a teapot.'],
                     '425': ['Client error responses','Too Early','Indicates that the server is unwilling to risk processing a request that might be replayed.'],
                     '426': ['Client error responses','Upgrade Required','The server refuses to perform the request using the current protocol but might be willing to do so after the client upgrades to a different protocol.'],
                     '428': ['Client error responses','Precondition Required','The origin server requires the request to be conditional. '],
                     '429': ['Client error responses','Too Many Requests','The user has sent too many requests in a given amount of time ("rate limiting").'],
                     '431': ['Client error responses','Request Header Fields Too Large','The server is unwilling to process the request because its header fields are too large. The request may be resubmitted after reducing the size of the request header fields.'],
                     '451': ['Client error responses','Unavailable For Legal Reasons','The user-agent requested a resource that cannot legally be provided, such as a web page censored by a government.'],
                     '500': ['Server error responses','Internal Server Error',"The server has encountered a situation it doesn't know how to handle."],
                     '501': ['Server error responses','Not Implemented','The request method is not supported by the server and cannot be handled.'],
                     '502': ['Server error responses','Bad Gateway','This error response means that the server, while working as a gateway to get a response needed to handle the request, got an invalid response'],
                     '503': ['Server error responses','Service Unavailable','The server is not ready to handle the request. Common causes are a server that is down for maintenance or that is overloaded.'],
                     '504': ['Server error responses','Gateway Timeout','This error response is given when the server is acting as a gateway and cannot get a response in time.'],
                     '505': ['Server error responses','HTTP Version Not Supported','The HTTP version used in the request is not supported by the server.'],
                     '506': ['Server error responses','Variant Also Negotiates','The server has an internal configuration error: the chosen variant resource is configured to engage in transparent content negotiation itself, and is therefore not a proper end point in the negotiation process.'],
                     '510': ['Server error responses','Not Extended','Further extensions to the request are required for the server to fulfil it.'],
                     '511': ['Server error responses','Network Authentication Required','The 511 status code indicates that the client needs to authenticate to gain network access.']
}

html_status_codes = pd.DataFrame.from_dict(html_status_codes).T.reset_index()
html_status_codes.columns = ['Status Code','Response Class','Short Description','Long Description']


'''                 RAW ASSETS                  '''
# Check File Type

raw_assets_path = files_grabbed_correct = ""

def file_type_check(now):
    global message_file_check, raw_assets_path, files_grabbed_correct
    os.chdir(raw_assets_path)
    list_files = os.listdir(raw_assets_path)
    types = ('*.gif', '*.png', '*.jpeg', '*.jpg')
    files_grabbed_correct = []
    for files1 in types:
        files_grabbed_correct.extend(glob.glob(files1))
    paths_grabbed_incorrect= set(list_files)- set(files_grabbed_correct)
    files_grabbed_incorrect = []
    for p in paths_grabbed_incorrect:
        if os.path.isfile(p): 
            files_grabbed_incorrect.append(p)
    final_directory_file_type_raw = raw_assets_path + '/incorrect_filetype_raw_tags' + '_' + now 
    n = len(files_grabbed_incorrect)
    if n > 0: 
        message_file_check = str(n) + " files were found to have incorrect types"
        if not os.path.exists(final_directory_file_type_raw):
            os.makedirs(final_directory_file_type_raw)  
        for f1 in files_grabbed_incorrect:
            shutil.copy(f1, final_directory_file_type_raw)
    return final_directory_file_type_raw
    
# Size no more than 150kb
    
def size_check(now):    
    global raw_assets_path,files_grabbed_correct, message_size_check
    os.chdir(raw_assets_path)
    check_file = [0]*len(files_grabbed_correct)
    for i in range(0,len(files_grabbed_correct)):
        if ((os.stat(files_grabbed_correct[i]).st_size/1000)<150):
            check_file[i]=0
        else:
            check_file[i]=files_grabbed_correct[i]   
            
    gif_files_oversized = [x for x in check_file if x != 0]
    final_directory_file_oversize = raw_assets_path + '/oversized_raw_tags' + '_' + now      
    n = len(gif_files_oversized)
    if n > 0: 
        if not os.path.exists(final_directory_file_oversize):
            os.makedirs(final_directory_file_oversize)
        for f in gif_files_oversized:
            shutil.copy(f, final_directory_file_oversize)
        message_size_check = str(n) + " files were found to be oversized."
    return final_directory_file_oversize
        
    
        
        
#Gifs Static after 30 seconds or not

def gif_static_30s_check(now):
    global raw_assets_path, files_grabbed_correct, message_gift_non_static
    os.chdir(raw_assets_path)
    im = [0]*len(files_grabbed_correct)
    check_static = [0]*len(files_grabbed_correct)
    ## Extracting the loop,duration and frames
    for i in range(0,len(files_grabbed_correct)):
        # To iterate through the entire gif
        try:
            im[i] = Image.open(files_grabbed_correct[i])
            loop = im[i].info["loop"]
            duration = im[i].info["duration"] 
            frames = im[i].tell()
            
            #Check the duration of gif
            load_time = loop * duration * frames /1000
            if (load_time > 30):
                check_static[i] = files_grabbed_correct[i]
            else:
                check_static[i] = 0
        except:
            pass # end 

    # Return values which are not static after 30 seconds - Raw Assets
    gif_files_non_static_post30 = [x for x in check_static if x != 0]
    
    #send the not static after 30 seconds into a folder
    final_directory_gif_static = raw_assets_path + '/30_sec_not_static_raw_tags' + '_' + now
    
    n = len(gif_files_non_static_post30)
    if n > 0:
        if not os.path.exists(final_directory_gif_static):
            os.makedirs(final_directory_gif_static)   
        for f2 in gif_files_non_static_post30:
            shutil.copy(f2, final_directory_gif_static)
        message_gift_non_static = str(n) + " GIF files were found to be high load times."
        
        

'''                 THIRD PARTY FILES               '''

def get_df_third_party(df_raw, filename, flag = 'csv/excel'):
    if flag == 'txt':
        placement_ids = re.findall('Placement ID: (.*)', df_raw)
        placement_names = re.findall('Placement Name: (.*)', df_raw)
        scripts = re.findall('(<script type="text/javascript">)(.*?)(</script>)', df_raw, flags = re.S)
        scripts_clean = []
        for disjointed_script in scripts:
            tag_code = ""
            for j in disjointed_script:
                tag_code += j
            scripts_clean.append(tag_code)
        df = pd.DataFrame(list(zip(placement_ids, placement_names, scripts_clean)), columns = ['Placement ID','Placement Name','JavaScript Tag'])
    else:   
        try:
            df_raw.columns = ["col_"+str(n) for n in range(df_raw.shape[1])]
            x_column = list(df_raw.loc[:,df_raw.isnull().sum() == df_raw.shape[0]].columns)
            df_raw = df_raw.drop(columns = x_column)
            #print(df_raw.shape)
        except:
            pass
        
        try:
            x_row = df_raw[df_raw.isnull().sum(axis=1) == 0].index[0]
            df_raw = df_raw.iloc[x_row:,:]
            #print(df_raw.shape)
        except:
            pass
        
        df_raw.columns = df_raw.iloc[0]
        df_raw = df_raw.drop(df_raw.index[0])
        # Run a try except here for different column names
        column_names = df_raw.columns.to_list()
        if all(x in column_names for x in ['Placement_ID','PlacementName','js_https']):
            df = df_raw[['Placement_ID','PlacementName','js_https']]
        elif all(x in column_names for x in ['Placement ID','Placement Name','JavaScript Tag']):
            df = df_raw[['Placement ID','Placement Name','JavaScript Tag']]
        elif all(x in column_names for x in ['Agency Placement ID','Agency Placement Name','Blocking Javascript Tag']):
            df = df_raw[['Agency Placement ID','Agency Placement Name','Blocking Javascript Tag']]
            
    # Once dataframes have been cleaned 
    
    df['tag_name'] = filename
    df.columns = ['placement_id','placement_name','tag_code','file_name']
    return df

def load_third_party_files(now):
    global third_party_path, missing_values_message
    os.chdir(third_party_path)
    df_cleaned = pd.DataFrame()
    csv_files = glob.glob('*.csv')
    if len(csv_files) > 0:
        for csv in csv_files:
            df_raw = pd.read_csv(csv)
            df = get_df_third_party(df_raw, csv)
            df_cleaned = df_cleaned.append(df)
    
    excel_files = glob.glob('*.xlsx') + glob.glob('*.xls')
    if len(excel_files) > 0:
        for excel in excel_files:
            df_raw = pd.read_excel(excel)
            df = get_df_third_party(df_raw, excel)
            df_cleaned = df_cleaned.append(df)
        
    text_files = glob.glob('*.txt')
    if len(text_files) > 0:
        for text in text_files:
            f = open(text, 'r')
            raw_text = f.read()
            df = get_df_third_party(raw_text, text, flag = 'txt')
            df_cleaned = df_cleaned.append(df)
        
    df_cleaned = df_cleaned.drop_duplicates()
    df_cleaned = df_cleaned.loc[df_cleaned['placement_id'].isnull() == False]
    missing_values = df_cleaned.loc[df_cleaned['tag_code'].isnull() == True]
    if missing_values.shape[0] > 0:
        n = str(len(missing_values))
        missing_values_directory = third_party_path + '\missing_values_' + now
        if not os.path.exists(missing_values_directory):
            os.makedirs(missing_values_directory)   
        
        os.chdir(missing_values_directory)
        missing_values.to_csv('placement_tags_with_missing_js_codes.csv',index = False)
        # Add a message box here
        missing_warning = tk.Toplevel()
        missing_warning.wm_withdraw()
        missing_values_message = n + " placement IDs have missing Javascript Tags."
        messagebox.showinfo(title="Missing Javascript Tags", message =  missing_values_message + "\nPlease check the root directory for the missing values files.")
        missing_warning.destroy()
        
    df_cleaned = df_cleaned.loc[df_cleaned['tag_code'].isnull() == False].reset_index(drop = True)
    df_cleaned['file_name'] = df_cleaned['file_name'].apply(lambda x: os.path.splitext(x)[0])
    df_cleaned['html_file_name'] = df_cleaned['file_name'] + '_' + df_cleaned['placement_id'].apply(lambda x: str(x)) + '.html'
    df_cleaned['html_file_name'] = df_cleaned['html_file_name'].apply(lambda x: x.replace(' ','_'))
    return missing_values_directory, df_cleaned

# Multiprocessing Landing Page
    
def worker1(h,template_path):
    app = Flask(__name__, template_folder = template_path)
    @app.route('/', methods=['GET', 'POST'])
    def index():
#        print("the hstring is " + h)
        return render_template(h)
    app.run()
 
def worker2(return_dict,h): 
    x = requests.get('http://127.0.0.1:5000/')
    if x.status_code == 200:
        print('All Good')
    else:
        print('Something is up')
    
    return_dict[h] = x.status_code
    

    
def update_progress_bar(page_progress,progress, value_queue):
    progress['value'] = value_queue
    page_progress.update()
    print(progress['value'])
        

def landing_page_check(df_cleaned,now):
    global message_incorrect_load,html_status_codes
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    template_path = third_party_path + '/templates'
    if not os.path.exists(template_path):
        os.makedirs(template_path)
    os.chdir(template_path)
    
    # Progress bar Screen Code
    page_progress = tk.Toplevel(root)
    s_title = tk.Label(page_progress, text = "Third Party Tag Progress", font="Calibri 14 bold italic",foreground = "white", background = "#2b0030", width = 50, height = 2)
    page_progress.configure(background = '#2b0030')
                     
    # Progress bar widget 
    progress = Progressbar(page_progress, orient = HORIZONTAL, length = 400, mode = 'determinate') 
    
    # Show final message after codes have run
    s_title.pack()
    progress.pack() 


    
    for index, row in df_cleaned.iterrows():
        html_str = row['tag_code']           
        Html_file= open(row['html_file_name'],"w")
        Html_file.write(html_str)
        Html_file.close()
    
    os.chdir(third_party_path)
    html_path = df_cleaned['html_file_name'].to_list()
    total_length = len(html_path)
    percent_done = 0
    count = 1
    for h in html_path:
        h_string = manager.Value(ctypes.c_char, h)
        
        # creating processes 
        percent_done = floor((count/total_length)*100)

        p1 = multiprocessing.Process(target=worker1, args = (h_string.value,template_path)) 
        p2 = multiprocessing.Process(target=worker2, args = (return_dict,h_string.value))
        count += 1
        
        # starting processes 
        p1.start() 
        p2.start() 

        
        # wait until processes are finished 
        p2.join() 
        p1.terminate()
        
        update_progress_bar(page_progress,progress, percent_done)
        
    
    
    third_party_status = dict(dict(return_dict))
    third_party_status = (pd.DataFrame(third_party_status, index = [0])).T
    third_party_status = third_party_status.reset_index()
    third_party_status.columns = ['filename_placementid','Status Code']
    htmls_loaded_incorrect = third_party_status.loc[third_party_status['Status Code'] != 200]
    
    htmls_loaded_incorrect = pd.merge(htmls_loaded_incorrect, html_status_codes, on = 'Status Code',how = 'left')
    
    htmls_loaded_incorrect = htmls_loaded_incorrect['filename_placementid'].to_list()
    final_directory_html_incorrect = third_party_path + '/htmls_loaded_incorrect_files' + '_' + now 
    n = len(htmls_loaded_incorrect)
    message = ""
    if n > 0: 
        message_incorrect_load = str(n) + " third party tags could not load." 
        message = message_incorrect_load + "\nPlease check the root directory for the incorrectly loaded tags."
        if not os.path.exists(final_directory_html_incorrect):
            os.makedirs(final_directory_html_incorrect)  
        htmls_loaded_incorrect.to_csv(final_directory_html_incorrect + '/incorrect_htmls.csv',index = False)
        for f1 in htmls_loaded_incorrect:
            shutil.copy(f1, final_directory_html_incorrect)
    else:
        message = 'All Tags Loaded Properly!'
        
    # Add a message box here
    incorrect_warning = tk.Toplevel()
    incorrect_warning.wm_withdraw()
    messagebox.showinfo(title="Third Party Tags Status", message = message)
    incorrect_warning.destroy()
    
    return final_directory_html_incorrect
    
def show_summary_report(message_file_check, message_size_check, message_gift_non_static,final_directory_file_type_raw,final_directory_file_oversize,final_directory_gif_static,
                        missing_values_message, message_incorrect_load, missing_values_directory,final_directory_html_incorrect):
    summary = "The QA is done. Summary report shown below. \n\n"
    """ RAW ASSETS """
    if path.exists(raw_assets_path):
        if len(message_file_check) > 0:
            summary += "\t\t" + message_file_check + " The incorrect files are stored in:\n\n" + final_directory_file_type_raw + "\n\n"
        if len(message_size_check) > 0:
            summary += "\t\t" + message_size_check + " The oversized files are stored in:\n\n" + final_directory_file_oversize + "\n\n"
        if len(message_gift_non_static) > 0:
            summary += "\t\t" + message_gift_non_static + " The non static GIF files are stored in:\n\n" + final_directory_gif_static + "\n\n"
            
        if len(message_file_check) == len(message_size_check) == len(message_gift_non_static) == 0:
            summary += "All raw assets have passed QA." + "\n\n"
        
    """ THIRD PARTY """
    if path.exists(third_party_path):
        if len(missing_values_message) > 0:
            summary += "\t\t" + missing_values_message + "The missing values file is stored in:\n\n" +  missing_values_directory + "\n\n"
        if len(message_incorrect_load) > 0:
            summary += "\t\t" + message_incorrect_load + "The oversized files are stored in:\n\n"  + final_directory_html_incorrect + "\n\n"
        else:
            summary += "\t\t" + "All third party tags have passed QA." + "\n\n"
            
    summary += "\nThank you for using the Creative QA Tool."
            
            
    # Summary Screen Code
    summary_window = tk.Toplevel(root)
    s_title = tk.Label(summary_window, text = "Report Summary", font="Calibri 14 bold italic",foreground = "white", background = "#2b0030", width = 50, height = 2)
    summary_window.configure(background = '#2b0030')
                     
    summary_text = scrolledtext.ScrolledText(summary_window, font="Calibri 12", foreground = "white", background = "#2b0030",height=10, width=100, borderwidth=0, highlightthickness=0)
    summary_text.insert(tk.END, summary)
    
    # Show final message after codes have run
    close_button = tk.Button(master = summary_window, text = "Quit", font="Calibri 12 bold", foreground = "#2b0030", background = "white", command=root.destroy)
    s_title.pack()
    summary_text.pack()
    close_button.pack()  
    

def qa_tool_main():
    # Allow user to select a directory and store it in a global var
    global root_directory, mypath, raw_assets_path, third_party_path
    filename = filedialog.askdirectory()
    root_directory.set(filename)
    mypath= root_directory.get()
    now = datetime.now()
    now = now.strftime("%d%m%Y%H%M%S")
    # Check Raw Assets
    raw_assets_path = mypath + '/raw_assets'
    final_directory_file_type_raw = final_directory_file_oversize = final_directory_gif_static = None
    if path.exists(raw_assets_path):
        final_directory_file_type_raw = file_type_check(now)
        final_directory_file_oversize = size_check(now)
        final_directory_gif_static = gif_static_30s_check(now)
        show_message(message_file_check, message_size_check, message_gift_non_static)
    else:
        print('No raw assets')
        
    # Check Third Party Tags
    third_party_path = mypath + '/ft_dcm_tags'
    missing_values_directory = final_directory_html_incorrect = None
    if path.exists(third_party_path):
        missing_values_directory,df_cleaned = load_third_party_files(now)
        ''' REMOVE THIS CODE FROM THE ACTUAL FILE '''
        df_cleaned = df_cleaned.loc[0:3,:]
        final_directory_html_incorrect = landing_page_check(df_cleaned, now)
    else:
        print('No third party tags')
        
    show_summary_report(message_file_check, message_size_check, message_gift_non_static,final_directory_file_type_raw,final_directory_file_oversize,final_directory_gif_static,
                        missing_values_message, message_incorrect_load, missing_values_directory,final_directory_html_incorrect)
    
    
    
""" MAIN FUNCTION """
                
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Creative QA Tool")
    #create the menubar
    menubar= Menu(root)
    root.config(menu= menubar)
    #create submenu 'File'
    submenu= Menu(menubar, tearoff= 0)
    menubar.add_cascade(label= "File", menu=submenu)
    
    def about_tool():
        tk.messagebox.showinfo('About Creative QA Tool', 'This is a tool built in Python')
        
    submenu.add_command(label= "About QA Tool", command= about_tool)
    submenu.add_command(label= "Close", command= root.destroy)
    
    #create submenu 'Help'
    submenu= Menu(menubar, tearoff= 0)
    menubar.add_cascade(label= "Help", menu=submenu)
        
    submenu.add_command(label= "FAQs", command= help_faqs)
    submenu.add_command(label= "Contact Us", command= help_contactus)
    
    # main screen code
    
    title = tk.Label(root, text = "Creative QA Tool", font="Calibri 20 bold italic",foreground = "white", background = "#2b0030", width = 50, height = 2)
    root.configure(background = '#2b0030')
                     
    intro_text = tk.Text(root, font="Calibri 14", foreground = "white", background = "#2b0030",height=7, width=70, borderwidth=0, highlightthickness=0)
    quote = """Hi! To use the tool most efficiently, please ensure that all third party tags are saved in a root directory and have the following sub directories (if available): 
    \t 1. /root-directory/raw_assets
    \t 2. /root-directory/ft_dcm_tags
    
    Please select your root directory.
    """
    intro_text.insert(tk.END, quote)
    
    # Show final message after codes have run
    message_file_check = message_size_check = message_gift_non_static = missing_values_message = message_incorrect_load = ""
    root_directory = tk.StringVar()
    browse_button = tk.Button(text = "Browse through computer", font="Calibri 12 bold", foreground = "#2b0030", background = "white", command=qa_tool_main)
    title.pack()
    intro_text.pack()
    browse_button.pack()  
    root.mainloop()

