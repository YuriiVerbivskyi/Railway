from flask import Flask
import threading, time, os, signal

PORT = int(os.environ.get("PORT", 7943))
app = Flask(__name__)
logs = []

def log(msg):
    logs.append(f"{msg}\n")
    if len(logs) > 100:
        logs.pop(0)
    print(msg, flush=True) 

def heartbeat():
    while True:
        log(time.strftime('%Y-%m-%d %H:%M:%S'))
        time.sleep(60)

@app.route("/")
def index():
    if not logs:
        return "<pre>Log is empty.</pre>"
    return "<pre>" + "".join(logs) + "</pre>"

@app.route("/kill")
def kill():
   log("KILL")
   os.kill(os.getpid(), signal.SIGTERM)

if __name__ == "__main__":
    threading.Thread(target=heartbeat, daemon=True).start()
    app.run(host="0.0.0.0", port=PORT)
