import requests
import json
import base64
# requests.post or .get, ...

# method GET api list object


def get(url):
    response = requests.get(url)
    return response.json()


def post(url, data):
    response = requests.post(url, data)
    return response.json()


if __name__ == '__main__':
    # API DANH SÁCH ĐỐI TƯỢNG
    BASE = 'https://gsdl-dev-api.greenglobal.vn/api/v1/ai/tour-guides'
    result = get(BASE)
    # GET DATA VA GHI
    '''
    with open('data.json', mode='w', encoding='utf-8') as outfile:
        json.dump(result, outfile)
    '''
    # DUYET VA PHAN LOAI DOI TUONG
    for i in range(len(result['data'])):
        data = result['data'][i]
        print('------LEGAL------\n')
        if data['attributes']['type'] == 'LEGAL':
            print(data)

        print('------ILLEGAL------\n')
        if data['attributes']['type'] == 'ILLEGAL':
            print(data)

        print('------OBJECT_TRACKED------\n')
        if data['attributes']['type'] == 'OBJECT_TRACKED':
            print(data)

    print('-'*50)
    # MO FILE DATA CAN GHI DANG JSON
    with open('datapost.json', mode='r', encoding='utf-8') as outfile:
        payload = json.load(outfile)
    print('PAYLOAD:\n')
    print(payload)
    # API GHI NHẬN DỮ LIỆU
    BASE1 = 'https://gsdl-dev-api.greenglobal.vn/api/v1/ai/events'
    print('RESPONSE:\n')
    print(post(BASE1, payload))
    print('-'*50)
    # API ĐẾM KHÁCH DU LỊCH
    BASE2 = 'https://gsdl-dev-api.greenglobal.vn/api/v1/number-of-tourists'
    with open('data_dem_khach.json', mode='r', encoding='utf-8') as outfile:
        payload = json.load(outfile)
    print('PAYLOAD:\n')
    print(payload)
    print('RESPONSE:\n')
    print(post(BASE2, payload))

    # UPLOAD FILE
    print('-'*50)
    url = 'https://gsdl-dev-api.greenglobal.vn/api/v1/upload'
    with open('confusionMatrix-percent.png', "rb") as f:
        im_bytes = f.read()
    im_b64 = base64.b64encode(im_bytes).decode("utf8")
    payload = json.dumps({'file': im_b64})
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    print(post(url, payload))

