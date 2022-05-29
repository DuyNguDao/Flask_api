import cv2
import requests
import io
import PIL.Image as Image
import json
import numpy as np


def try_request(method=None, url=None, **kwargs):
    success = False
    ret = None
    exception = None

    try:
        ret = requests.request(method, url, **kwargs)
        success = True
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        exception = "Timeout"
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        exception = "TooManyRedirects"
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        exception = e

    return [success, ret, exception]


def get_limit_page(limit, page):
    """
    API GET THÔNG TIN CỦA LIMIT VÀ PAGE
    :param limit: limit
    :param page: page
    :return: json
    """
    params = {'limit': limit, 'page': page}
    url = 'https://gsdl-dev-api.greenglobal.vn/api/v1/ai/objects'
    success, ret, exception = try_request(method='GET', url=url, params=params)
    if success:
        response = ret.json()
    else:
        response = None

    return {'req_success': success, 'response': response, 'exception': exception}


def get_all_data(limit):

    """
    API GET TẤT CẢ CÁC DỮ LIỆU CỦA MỘT LIMIT
    :param limit: limit
    :return: list data
    """
    ret = get_limit_page(limit=1, page=1)
    req_success = ret['req_success']
    response = ret['response']
    exception = ret['exception']
    data = []
    if not req_success:
        print("Thực hiện request đến VMS-Server thất bại ({})".format(str(exception)))
    else:
        # cần xử lý gói xử lý trả về từ server cho biết kết quả X có thành công hay không
        if response['status'] == 200:

            result_pagination = response['meta']['pagination']
            total = result_pagination['total']
            for i in range(1, int(total/limit) + 2):
                ret = get_limit_page(limit, i)
                req_success = ret['req_success']
                response = ret['response']
                exception = ret['exception']
                if not req_success:
                    print("Thực hiện request đến VMS-Server thất bại ({})".format(str(exception)))
                else:
                    # cần xử lý gói xử lý trả về từ server cho biết kết quả X có thành công hay không
                    data.extend(response['data'])
        else:
            print(response['status'])
            print(response['title'])
    return data


def post_image(path_image):
    """
    API UPLOAD FILE IMAGE
    :param path_image: path of image
    :return: response json
    """
    url = 'https://gsdl-dev-api.greenglobal.vn/api/v1/upload'
    files = {'file': open(path_image, 'rb')}
    success, ret, exception = try_request(method='POST', url=url, files=files)
    if success:
        response = ret.json()
    else:
        response = None
    return {'req_success': success, 'response': response, 'exception': exception}


def post_video(path_video):
    """
    API UPLOAD FILE VIDEO
    :param path_video: path of video
    :return: response json
    """
    url = 'https://gsdl-dev-api.greenglobal.vn/api/v1/upload'
    files = {'file': (path_video, open(path_video, 'rb'))}
    success, ret, exception = try_request(method='POST', url=url, files=files)
    if success:
        response = ret.json()
    else:
        response = None
    return {'req_success': success, 'response': response, 'exception': exception}


def post_data(payload):
    """
    API GHI NHẬN DỮ LIỆU
    :param payload:
                event_code:             mã loại sự kiện
                                        HDVHP :  Phát hiện đối tượng hướng dẫn viên hợp pháp
                                        HDVBHP :  Phát hiện đối tượng hướng dẫn viên bất hợp pháp
                                        BL: Phát hiện đối tượng cần theo dõi
                                        NNHDV:  Phát hiện đối tượng nghi ngờ là hướng dẫn viên
                                        HVHD: Phát hiện hành vi hướng dẫn
                                        BHR:  Phát hiện hành vi bán hàng rong
                                        RAC: Phát hiện rác
                time:                   thời gian diễn ra sự kiện
                object_id:              id đối tượng
                object_type:            loại đối tượng
                camera_id:              id camera quan sát
                track_id:               id tracking của bên AI
                percent_similarity:     Độ chính xác
                image_path:             hình ảnh quan sát
                video_path:             video quan sát
                related_images:         mảng các hình ảnh bổ sung khả năng training
    :return:
    """
    url = 'https://gsdl-dev-api.greenglobal.vn/api/v1/ai/events'
    success, ret, exception = try_request(method='POST', url=url, data=payload)
    if success:
        response = ret.json()
    else:
        response = None
    return {'req_success': success, 'response': response, 'exception': exception}


def get_image(path):
    """
    API GET FILE ẢNH
    :param path: path image
    :return: image
    """
    url = "https://gsdl-dev-storage.greenglobal.vn/dltm/" + path
    success, ret, exception = try_request(method='GET', url=url)
    if success:
        response = ret.content
    else:
        response = None
    return {'req_success': success, 'response': response, 'exception': exception}


def get_video(path):
    """
    API GET FILE VIDEO
    :param path: path video
    :return: video
    """
    url = "https://gsdl-dev-storage.greenglobal.vn/dltm/" + path
    response = requests.get(url=url, stream=True)
    data = response.content


def post_number_of_tourist(payload):
    """
    API ĐẾM SỐ LƯỢNG KHÁCH DU LỊCH
    :param payload:
                camera_id:              id camera quan sát
                time:                   thời gian xảy ra sự kiện
                number_of_guest_in:     số lượng khách vào
                number_of_guest_out:    số lượng khách ra
    :example payload = {"camera_id" : "55ef5ba5-b5a7-482b-a513-85594ff99266",
                        "time": "2021-12-01 08:00:00",
                        "number_of_guest_in" : 10,
                        "number_of_guest_out" : 15}
    :return: data json
    """

    url = "https://gsdl-dev-api.greenglobal.vn/api/v1/ai/number-of-tourists"
    success, ret, exception = try_request(method='POST', url=url, data=payload)
    if success:
        response = ret.json()
    else:
        response = None
    return {'req_success': success, 'response': response, 'exception': exception}


if __name__ == '__main__':

    # GET ALL DATA
    data = get_all_data(limit=1)
    print(data)

    # POST IMAGE
    ret = post_image('index.jpg')
    req_success = ret['req_success']
    response_image = ret['response']
    exception = ret['exception']
    data = []
    if not req_success:
        print("Thực hiện request đến VMS-Server thất bại ({})".format(str(exception)))
    else:
        # cần xử lý gói xử lý trả về từ server cho biết kết quả X có thành công hay không
        print(response_image)

    # POST VIDEO
    ret = post_video('video.mp4')
    req_success = ret['req_success']
    response_video = ret['response']
    exception = ret['exception']
    data = []
    if not req_success:
        print("Thực hiện request đến VMS-Server thất bại ({})".format(str(exception)))
    else:
        # cần xử lý gói xử lý trả về từ server cho biết kết quả X có thành công hay không
        print(response_video)

    # POST DATA
    payload = {
                "event_code": "HDVHP",
                "time": "2021-01-01 08:00:01",
                "object_id": "7b98446c-2ef1-4c10-9487-41e008cda203",
                "object_type": "LEGAL",
                "camera_id": "7b98446c-2ef1-4c10-9487-41e008cda203",
                "track_id": "7b98446c-2ef1-4c10-9487-41e008cda203",
                "percent_similarity": "70.25",
                "image_path": response_image['path'],
                "video_path": response_video['path'],
                "related_images": [
                {
                    "path": response_image['path'],
                    "vector": "string"
                },
                {
                    "path": response_image['path'],
                    "vector": "string"
                }
                ]
            }

    ret = post_data(payload)
    req_success = ret['req_success']
    response_data = ret['response']
    exception = ret['exception']
    data = []
    if not req_success:
        print("Thực hiện request đến VMS-Server thất bại ({})".format(str(exception)))
    else:
        # cần xử lý gói xử lý trả về từ server cho biết kết quả X có thành công hay không
        print(response_data)

    # GET IMAGE
    ret = get_image(response_image['path'])
    req_success = ret['req_success']
    response = ret['response']
    exception = ret['exception']
    data = []
    if not req_success:
        print("Thực hiện request đến VMS-Server thất bại ({})".format(str(exception)))
    else:
        # cần xử lý gói xử lý trả về từ server cho biết kết quả X có thành công hay không
        image = Image.open(io.BytesIO(response))
        image_array = np.array(image)
        #cv2.imshow('image', image_array)
        #cv2.waitKey(0)

    # GET VIDEO
    get_video(response_video['path'])

    # POST NUMBER OF TOURIST
    payload = {
               "camera_id": "55ef5ba5-b5a7-482b-a513-85594ff99266",
               "time": "2021-12-01 08:00:00",
               "number_of_guest_in": 10,
               "number_of_guest_out": 15}
    ret = post_number_of_tourist(payload)
    req_success = ret['req_success']
    response_data = ret['response']
    exception = ret['exception']
    data = []
    if not req_success:
        print("Thực hiện request đến VMS-Server thất bại ({})".format(str(exception)))
    else:
        # cần xử lý gói xử lý trả về từ server cho biết kết quả X có thành công hay không
        print(response_data)
        if response_data['status'] == 201:
            print(response_data)
        else:
            print(response_data['status'])
            print(response_data['title'])


