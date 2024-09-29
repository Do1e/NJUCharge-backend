import json
import queue
import threading
import time

# from utils.per_station import get_outlets
from utils.per_outlet import get_outlet_status

debug = False

with open('status.json', 'r', encoding='utf-8') as f:
    status = json.load(f)

def update_station(station, idx, debug=False, result_queue=None):
    station_id = station['id']

    # outlets = get_outlets(station_id, debug=debug) # 如果配置了token.txt，可以直接调用这个函数
    outlets = status[idx]['outlets']
    outlets = [outlet['id'] for outlet in outlets]

    outlets_status = []
    for outlet_id in outlets:
        outlet_status = get_outlet_status(outlet_id, debug=debug)
        if outlet_status:
            outlets_status.append(outlet_status)
        time.sleep(0.5)
    if result_queue is not None:
        result_queue.put((idx, outlets_status))

result_queue = queue.Queue()
threads = []
for i, station in enumerate(status):
    t = threading.Thread(target=update_station, args=(station, i, debug, result_queue))
    threads.append(t)
    t.start()

for i, t in enumerate(threads):
    t.join()

while not result_queue.empty():
    idx, outlets_status = result_queue.get()
    status[idx]['outlets'] = outlets_status

with open('status.json', 'w', encoding='utf-8') as f:
    json.dump(status, f, ensure_ascii=False, indent=2)
