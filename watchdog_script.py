from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
import subprocess

class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.start_server()

    def start_server(self):
        self.process = subprocess.Popen(['python', 'app.py'])

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f'Event type: {event.event_type}  path : {event.src_path}')
            self.process.terminate()
            self.process.wait()
            self.start_server()

event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path='.', recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
    observer.join()
    event_handler.process.terminate()
