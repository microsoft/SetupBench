
import os
import time
import json
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_PATH = os.environ.get("WATCH_PATH", "/watched")
LOG_PATH = "/var/log/watcher.json.log"

class WatchHandler(FileSystemEventHandler):
    def process(self, event_type, src_path):
        log_entry = {
            "event": event_type,
            "path": src_path,
            "timestamp": datetime.utcnow().isoformat()
        }
        with open(LOG_PATH, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    def on_created(self, event):
        if not event.is_directory:
            self.process("created", event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.process("modified", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self.process("deleted", event.src_path)

if __name__ == "__main__":
    os.makedirs(WATCH_PATH, exist_ok=True)
    event_handler = WatchHandler()
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_PATH, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
