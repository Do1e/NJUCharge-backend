import requests
import datetime
import time

def get_outlet_status(outlet_id, debug=False):
    url = f'https://wemp.issks.com/charge/v1/charging/outlet/{outlet_id}'
    resp = requests.get(url)
    ts = int(time.time())
    try:
        resp = resp.json()
        if not resp['success']:
            return {}
        name = resp['data']['station']['vStationName'] + ' ' + resp['data']['outlet']['vOutletName']
        if resp['data']['station']['hardWareState'] != 1 or resp['data']['outlet']['iErrorCount'] != 0:
            error = True
        else:
            error = False
        status = resp['data']['nowBillingType']
        if status == 0:
            msg = '空闲' if not error else '故障'
        elif status == 1:
            msg = '分钟计费模式'
        elif status == 4:
            msg = '固定金额模式'
        elif status == 5:
            msg = '电度计费模式'
        else:
            msg = '未知'
        usedmin = resp['data']['usedmin']
        if msg == '空闲':
            restmin = 0
        elif status == 1:
            feePerHour = float(resp['data']['powerFee']['billingFee'].replace('元/小时', ''))
            feePerMinute = 0
            for item in resp['data']['billListDtoList'][0]['propertyList']:
                if abs(item['dFeePerHour'] - feePerHour) < 1e-6:
                    feePerMinute = item['dFeePerMin']
                    break
            if feePerMinute == 0:
                restmin = 65535
            else:
                restmin = int((resp['data']['userSelectAmount'] - resp['data']['usedfee']) / feePerMinute)
        elif status == 4:
            restmin = resp['data']['restmin']
        else:
            restmin = 65535
        if status == 1 or status == 4:
            available_time = datetime.datetime.now() + datetime.timedelta(minutes=restmin)
            available_time = available_time.strftime('%m-%d %H:%M')
        elif status == 0 and not error:
            available_time = 'now'
        else:
            available_time = 'unknown'
        return {
            'id': outlet_id,
            'name': name,
            'restmin': restmin,
            'usedmin': usedmin,
            'error': error,
            'status': status,
            'msg': msg,
            'available_time': available_time,
            'update_time': ts,
        }
    except:
        if debug:
            if hasattr(resp, 'text'):
                print(resp.text)
            else:
                print(resp)
            raise
        return {}

if __name__ == '__main__':
    station_id = '158789'
    from per_station import get_outlets
    outlets = get_outlets(station_id)
    for outlet_id in outlets:
        print(get_outlet_status(outlet_id))
