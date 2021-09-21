import threading
import time
from flask import Flask, render_template
import requests

exitFlag = 0
app = Flask(__name__)

class myThread_render_template(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        print('Initialised ' + name )
    @app.route('/', methods=['GET', 'POST'])
    def index():
        return render_template('a.html')

class myThread_check_status_code(threading.Thread):
    @app.route('/', methods=['GET', 'POST'])
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        print('Initialised ' + name )     
    def check_status_code():
        time.sleep(10)
        x = requests.get('http://127.0.0.1:5000/')
        print(x.status_code)
        print(x.text)
    



if __name__ == "__main__":
    # Create new threads
    thread1 = myThread_render_template("Thread - Flask")
    thread2 = myThread_check_status_code("Thread - Requests")
    
    # Start new Threads
    thread1.start()
    thread2.start()
    
    print("Exiting Main Thread")
