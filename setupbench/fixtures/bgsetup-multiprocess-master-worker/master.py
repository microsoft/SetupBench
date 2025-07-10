
import os
import time
from datetime import datetime

os.makedirs("/queue", exist_ok=True)

i = 0
while True:
    job_name = f"job_{i}.txt"
    job_path = os.path.join("/queue", job_name)
    with open(job_path, "w") as f:
        f.write(f"Job created at {datetime.utcnow().isoformat()}")
    i += 1
    time.sleep(10)
