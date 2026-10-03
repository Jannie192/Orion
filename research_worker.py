import json
import os
import time
import urllib.request

SUPABASE_URL = os.environ["SUPABASE_URL"].rstrip("/")
SUPABASE_KEY = os.environ["SUPABASE_PUBLISHABLE_KEY"]
DISPATCH_URL = SUPABASE_URL + "/functions/v1/orion-research-dispatch"
INTERVAL = int(os.environ.get("ORION_RESEARCH_POLL_SECONDS", "15"))

def call_dispatch():
    req = urllib.request.Request(
        DISPATCH_URL,
        data=json.dumps({"source": "orion-research-worker"}).encode(),
        headers={
            "apikey": SUPABASE_KEY,
            "Content-Type": "application/json",
            "x-orion-worker-role": "orion-research-worker-v1",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as response:
        return json.loads(response.read().decode())

print("ORION research worker started", flush=True)

while True:
    try:
        result = call_dispatch()
        if result.get("processed"):
            print("Processed research request:", result.get("request"), flush=True)
        elif result.get("idle"):
            print("Research queue idle", flush=True)
        else:
            print("Worker response:", result, flush=True)
    except Exception as exc:
        print("Worker error:", exc, flush=True)
    time.sleep(INTERVAL)
