import requests
import json
import PIL.Image as Image
import io
import cv2
import numpy as np


class API:
    def get_limit_page(self, limit, page):
        """
        API GET THÔNG TIN CỦA LIMIT VÀ PAGE
        :param limit: limit
        :param page: page
        :return: json
        """
        params = {'limit': limit,
                  'page': page}
        url = 'https://gsdl-dev-api.greenglobal.vn/api/v1/ai/tour-guides'
        response = requests.get(url=url, params=params)
        return response.json()

    def get_all_data(self, limit):

        """
        API GET TẤT CẢ CÁC DỮ LIỆU CỦA MỘT LIMIT
        :param limit: limit
        :return: list data
        """
        result = self.get_limit_page(limit=1, page=1)
        result_pagination = result['meta']['pagination']
        total = result_pagination['total']
        data = []
        for i in range(1, int(total/limit) + 2):
            data.extend(self.get_limit_page(limit, i)['data'])
        return data

    def post_image(self, path_image):
        """
        API UPLOAD FILE IMAGE
        :param path_image: path of image
        :return: response json
        """
        url = 'https://gsdl-dev-api.greenglobal.vn/api/v1/upload'
        payload = {'file': open(path_image, 'rb')}
        result_post = requests.post(url=url, files=payload)
        response = result_post.json()
        return response

    def post_video(self, path_video):
        """
        API UPLOAD FILE VIDEO
        :param path_video: path of video
        :return: response json
        """
        url = 'https://gsdl-dev-api.greenglobal.vn/api/v1/upload'
        payload = {'file': (path_video, open(path_video, 'rb'))}
        result_post = requests.post(url=url, files=payload)
        response = result_post.json()
        return response

    def post_data(self, payload):
        """
        API GHI NHẬN DỮ LIỆU
        :param payload:
                event_type_id:          id loại sự kiện
                tourist_destination_id: id khu điểm
                warning_level:          mức độ cảnh báo (LOW, MEDIUM, HIGH, EMERGENCY)
                time:                   thời gian diễn ra sự kiện
                tour_guide_id:          id đối tượng
                camera_id:              id camera quan sát
                image_path:             hình ảnh quan sát
                video_path:             video quan sát
        :return:
        """
        url = 'https://gsdl-dev-api.greenglobal.vn/api/v1/ai/events'
        response = requests.post(url=url, data=payload)
        return response.json()

    def get_image(self, path):
        """
        API GET FILE ẢNH
        :param path: path image
        :return: image
        """
        url = "https://gsdl-dev-storage.greenglobal.vn/dltm/" + path
        response = requests.get(url=url).content
        image = Image.open(io.BytesIO(response))
        return image

    def get_video(self, path):
        """
        API GET FILE VIDEO
        :param path: path video
        :return: video
        """
        url = "https://gsdl-dev-storage.greenglobal.vn/dltm/" + path
        response = requests.get(url=url).content
        return io.BytesIO(response)

    def post_number_of_tourist(self, payload):
        """
        API ĐẾM SỐ LƯỢNG KHÁCH DU LỊCH
        :param payload:
                camera_id:              id camera quan sát
                tourist_destination_id: id khu điểm
                time:                   thời gian xảy ra sự kiện
                number_of_guest:        số lượng khách
        :example payload = {"camera_id" : "55ef5ba5-b5a7-482b-a513-85594ff99266",
                            "tourist_destination_id" :"55ef5ba5-b5a7-482b-a513-85594ff99266",
                            "time": "2021-12-01 08:00:00",
                            "number_of_guest" : 10}
        :return: data json
        """

        url = "https://gsdl-dev-api.greenglobal.vn/api/v1/ai/number-of-tourists"
        response = requests.post(url=url, data=payload)
        return response.json()


if __name__ == '__main__':
    # start api
    api = API()
    # *********************************************************
    # GET ALL DATA
    data = api.get_all_data(limit=4)
    print(data)
    print('*'*50)
    # *********************************************************
    # POST IMAGE
    path_image = 'index.jpg'
    response_image = api.post_image(path_image)
    print(response_image)
    print('*'*50)
    # *********************************************************
    # POST VIDEO
    path_video = 'video.mp4'
    response_video = api.post_video(path_video)
    print(response_video)
    print('*'*50)
    # *********************************************************
    # POST DATA
    payload = {
        "event_type_id": "4aa58748-a62b-4b31-b303-7f5f6e03d037",
        "tourist_destination_id": "55ef5ba5-b5a7-482b-a513-85594ff99266",
        "warning_level": "HIGH",
        "time": "2021-01-01 08:00:01",
        "tour_guide_id": "7b98446c-2ef1-4c10-9487-41e008cda203",
        "camera_id": "7b98446c-2ef1-4c10-9487-41e008cda203",
        "image_path": response_image['path'],
        "video_path": response_video['path']}
    response_data = api.post_data(payload)
    print(response_data)
    print('*'*50)
    # *********************************************************
    # POST NUMER OF TOURIST
    payload = {
        "camera_id": "55ef5ba5-b5a7-482b-a513-85594ff99266",
        "tourist_destination_id": "55ef5ba5-b5a7-482b-a513-85594ff99266",
        "time": "2021-12-01 08:00:00",
        "number_of_guest": 10}
    response_tourist = api.post_number_of_tourist(payload)
    print(response_tourist)
    print('*'*50)
    # *********************************************************
    # GET FILE IMAGE
    # get image
    image = api.get_image(response_image['path'])
    # convert string -> array
    image_array = np.array(image)
    # cv2.imshow('image', image_array)
    # cv2.waitKey(0)
    print('*'*50)
    # *********************************************************
    # GET VIDEO
    video = api.get_video(response_video['path'])
    video = np.array(video)
    print(video)
