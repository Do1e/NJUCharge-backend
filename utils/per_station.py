import requests

with open('token.txt') as f:
    token = f.read().strip()
    # 需要自行抓包，在闪开来电返回的Header中找到token项

def get_outlets(station_id, debug=False):
    url = f'https://wemp.issks.com/charge/v1/outlet/station/outlets/{station_id}'
    resp = requests.get(url, headers={'token': token})
    try:
        resp = resp.json()
        if not resp['success']:
            return []
        outlets = [item['outletNo'] for item in resp['data']]
        return outlets
    except:
        if debug:
            if hasattr(resp, 'text'):
                print(resp.text)
            else:
                print(resp)
            raise
        return []

if __name__ == '__main__':
    station_id = '117375'
    print(get_outlets(station_id))
