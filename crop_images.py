from mtcnn.mtcnn import MTCNN
import cv2
import os
import json

# import h5py
# print(h5py.__version__)
PATH_IMAGE = './images'
PATH_CROP_MARGIN = './crop_margin'
PATH_CROP_STANDARD = './crop_standard'


# TODO: input: path of image -> output: bounding box & landmark
def mtcnn(path_images):
    img = cv2.imread(path_images)
    detector = MTCNN()
    return detector.detect_faces(img)


def crop_image(img, detect_faces, path_save, isMargin):
    i = 0
    print(detect_faces)
    for face in detect_faces:
        confidence = face['confidence']
        if confidence < 0.95:
            continue
        i += 1
        bounding_box = face['box']

        x = bounding_box[0]
        y = bounding_box[1]
        w = bounding_box[2]
        h = bounding_box[3]

        height, width, channels = img.shape
        if isMargin:
            x = bounding_box[0] - int(bounding_box[2] / 3)
            y = bounding_box[1] - int(bounding_box[3] / 3)
            w = bounding_box[2] + 2 * int(bounding_box[2] / 3) + 1
            h = bounding_box[3] + 2 * int(bounding_box[3] / 3) + 1
            if x < 0:
                x = 0
            if y < 0:
                y = 0
            if w > width:
                w = width
            if h > height:
                h = height
        # else:
        #     x = bounding_box[0] - int(bounding_box[2] / 3)
        #     y = bounding_box[1] - int(bounding_box[3] / 3)
        #     w = bounding_box[2]
        #     h = bounding_box[3]
        crop_img = img[y:y + h, x:x + w]
        crop_img = cv2.resize(crop_img, (160, 160))
        cv2.imwrite(path_save + '_' + str(i) + '.png', crop_img)


def crop_all_images(path_read, path_write, isMargin):
    files = os.listdir(path_read)
    for file in files:
        images = os.listdir(path_read + '/' + file)
        if not os.path.exists(path_write + '/' + file):
            os.makedirs(path_write + '/' + file)
        for image in images:
            print(path_read + '/' + file + '/' + image)
            path_save = path_write + '/' + file + '/' + image.split('.')[0]
            img = cv2.imread(path_read + '/' + file + '/' + image)
            crop_image(img, mtcnn(path_read + '/' + file + '/' + image), path_save, isMargin)


def export_data_json(path):
    files = os.listdir(path)
    for file in files:
        dictionary = {
        }
        images = os.listdir(path + '/' + file)
        for image in images:
            bounding_box = mtcnn(path + '/' + file + '/' + image)
            print(path + '/' + file + '/' + image)
            if len(bounding_box) > 0:
                dictionary[image] = bounding_box[0]['box']
        with open('./jsondata/' + file + '.json', 'w') as outfile:
            json.dump(dictionary, outfile)


# crop_all_images(path_read=PATH_IMAGE, path_write=PATH_CROP_MARGIN, isMargin=True)
# crop_all_images(path_read=PATH_CROP_MARGIN, path_write=PATH_CROP_STANDARD, isMargin=False)
export_data_json(PATH_CROP_MARGIN)
