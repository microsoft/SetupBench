
import os
import time
import shutil

os.makedirs("/queue", exist_ok=True)
os.makedirs("/processed", exist_ok=True)

while True:
    for filename in os.listdir("/queue"):
        src = os.path.join("/queue", filename)
        dst = os.path.join("/processed", filename)
        shutil.move(src, dst)
        with open("/var/log/processed.log", "a") as log_file:
            log_file.write(f"Processed {filename}\n")
    time.sleep(5)
