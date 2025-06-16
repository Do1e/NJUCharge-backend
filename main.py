import json
import queue
import threading
import os
from copy import deepcopy

from utils.per_station import get_outlets
from utils.per_outlet import get_outlet_status


def update_station(station, idx, debug=False, result_queue=None):
    station_id = station['id']
    outlets = get_outlets(station_id, debug=debug)
    outlets_status = []
    for outlet_id in outlets:
        outlet_status = {}
        trytimes = 5
        while not outlet_status:
            outlet_status = get_outlet_status(outlet_id, debug=debug)
            trytimes -= 1
            if trytimes == 0:
                break
        if outlet_status:
            outlets_status.append(outlet_status)
    if result_queue is not None:
        result_queue.put((idx, outlets_status))

def main(campus: str = 'all', debug: bool = False):
    with open('stations.json', 'r', encoding='utf-8') as f:
        stations = json.load(f)
    if campus != 'all':
        stations = [station for station in stations if station['campus'] == campus]

    result_queue = queue.Queue()
    threads = []
    for i, station in enumerate(stations):
        t = threading.Thread(target=update_station, args=(station, i, debug, result_queue))
        threads.append(t)
        t.start()

    for i, t in enumerate(threads):
        t.join()

    status = deepcopy(stations)
    while not result_queue.empty():
        idx, outlets_status = result_queue.get()
        status[idx]['outlets'] = outlets_status

    if not os.path.exists('output'):
        os.makedirs('output')
    with open(f'output/status_{campus}.json', 'w', encoding='utf-8') as f:
        json.dump(status, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Update all stations status')
    parser.add_argument('--campus', type=str, default='all', help='Campus name (default: all)')
    parser.add_argument('--debug', action='store_true', help='Debug mode (default: False)')
    args = parser.parse_args()
    main(campus=args.campus, debug=args.debug)
