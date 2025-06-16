import json
import time

def main(campus: str = 'all'):
    with open(f'output/status_{campus}.json', 'r', encoding='utf-8') as f:
        status = json.load(f)

    # sort by restmin
    outlets = []
    for station in status:
        for outlet in station['outlets']:
            outlet['station'] = {'id': station['id'], 'name': station['name']}
            outlet['update_time'] = time.strftime('%m-%d %H:%M:%S', time.localtime(outlet['update_time']))
            outlet_name = outlet['name'].split(' ')[1]
            station_name = station['name']
            outlet['name'] = station_name.split('-')[1] + ' ' + outlet_name
            outlet['station'] = station_name.split('-')[0]
            outlet['campus'] = station['campus']
            # outlet['name'] = outlet['name']
            # outlet['station'] = station['name']
            outlets.append(outlet)

    def sort_key(outlet):
        msg_priority = {
            '空闲': 0,
            '固定金额模式': 1,
            '分钟计费模式': 2,
            '电度计费模式': 2,
            '故障': 3,
            '未知': 4
        }
        return (msg_priority.get(outlet['msg'], 5), outlet['restmin'], -outlet['usedmin'])

    outlets.sort(key=sort_key)
    with open(f'output/outlets_{campus}.json', 'w', encoding='utf-8') as f:
        json.dump(outlets, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Update all stations status')
    parser.add_argument('--campus', type=str, default='all', help='Campus name (default: all)')
    args = parser.parse_args()
    main(campus=args.campus)
