import face_recognition
# import os
# import cv2
#
from PIL import Image
from make_deerace_photo import *
import os

class DeERace():
    def __init__(self, images_with_photo_path, photo_name, user_dir_path):
        self.images_with_photo_path = images_with_photo_path
        self.images_with_face_path_list = [] # List of files with faces
        self.photo_name = photo_name
        self.user_dir_path = user_dir_path


    def __del__(self):
        print()

    def find_face_and_processing(self):
        input_image_numpy = face_recognition.load_image_file(self.images_with_photo_path)

        face_locations_list = face_recognition.face_locations(input_image_numpy)
        print("I found {} face(s) in this photograph.".format(len(face_locations_list)))


        # self.images_with_photo_path + "_" + str(index_num) + ".jpg"
        deerace_project_name = self.photo_name # name for forlders of this deerace project

        folder_for_deerace = self.user_dir_path + "deerace/"
        folder_for_deerace_results = self.user_dir_path + "deerace/results/" + deerace_project_name + "/"
        folder_for_face_images_path = self.user_dir_path + "deerace/datasets/" + deerace_project_name + "/testA/"
        if os.path.isdir(folder_for_face_images_path) == False:
            mode = 0o755
            os.makedirs(folder_for_face_images_path, mode)  # dicrectory for current user
        if os.path.isdir(folder_for_deerace_results) == False:
            os.makedirs(folder_for_deerace_results, mode)  # dicrectory for current user


        index_num = 0
        for face_location in face_locations_list:

            # Print the location of each face in this image
            top, right, bottom, left = face_location
            print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

            #############################################
            ############Resize coordinates###############
            delta_coefficient = 0.5

            delta_top_buttom = int(round((bottom - top) * delta_coefficient))
            delta_left_right = int(round((right - left) * delta_coefficient))

            image_height, image_width, _ = input_image_numpy.shape

            top = top - delta_top_buttom
            if top < 0:
                top = 0

            bottom = bottom + delta_top_buttom
            if bottom > image_height:
                bottom = image_height

            left = left - delta_left_right
            if left < 0:
                left = 0

            right = right + delta_left_right
            if right > image_width:
                right = image_width
            ############Resize coordinates###############
            #############################################
            print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

            #face_image_path = self.images_with_photo_path + "_" + str(index_num) + ".jpg"
            face_image_path = folder_for_face_images_path + "face_" + str(index_num) + ".jpg"
            index_num += 1

            image_size = 256, 256

            # You can access the actual face itself like this:
            face_image_numpy = input_image_numpy[top:bottom, left:right]
            pil_image = Image.fromarray(face_image_numpy)
            self.resize_and_crop(face_image_path, image_size, crop_type='middle', img=pil_image)
            #pil_image.thumbnail(image_size, Image.ANTIALIAS)
            #pil_image.save(face_image_path, "JPEG")
            self.images_with_face_path_list.append(face_image_path)

        deerace_result = make_deerace_photo(project_name="deerace", data_root_path=folder_for_face_images_path,
                                            results_dir=folder_for_deerace_results)
        print(deerace_result)
        for dict_from_list in deerace_result:
            for keys_from_dict in dict_from_list.keys():
                print(dict_from_list[keys_from_dict]['real'])
                print(dict_from_list[keys_from_dict]['fake'])
                print()

        return len(self.images_with_face_path_list), deerace_result

    def resize_and_crop(self, modified_path, size, crop_type='top', img_path=None, img=None):
        """
        Resize and crop an image to fit the specified size.

        args:
        img_path: path for the image to resize.
        modified_path: path to store the modified image.
        size: `(width, height)` tuple.
        crop_type: can be 'top', 'middle' or 'bottom', depending on this
        value, the image will cropped getting the 'top/left', 'middle' or
        'bottom/right' of the image to fit the size.
        raises:
        Exception: if can not open the file in img_path of there is problems
        to save the image.
        ValueError: if an invalid `crop_type` is provided.
        """
        # If height is higher we resize vertically, if not we resize horizontally
        if img_path != None:
            img = Image.open(img_path)
        # Get current and desired ratio for the images
        img_ratio = img.size[0] / float(img.size[1])
        ratio = size[0] / float(size[1])
        # The image is scaled/cropped vertically or horizontally depending on the ratio
        if ratio > img_ratio:
            img = img.resize((size[0], int(round(size[0] * img.size[1] / img.size[0]))),
                             Image.ANTIALIAS)
            # Crop in the top, middle or bottom
            if crop_type == 'top':
                box = (0, 0, img.size[0], size[1])
            elif crop_type == 'middle':
                box = (0, int(round((img.size[1] - size[1]) / 2)), img.size[0],
                       int(round((img.size[1] + size[1]) / 2)))
            elif crop_type == 'bottom':
                box = (0, img.size[1] - size[1], img.size[0], img.size[1])
            else:
                raise ValueError('ERROR: invalid value for crop_type')
            img = img.crop(box)
        elif ratio < img_ratio:
            img = img.resize((int(round(size[1] * img.size[0] / img.size[1])), size[1]),
                             Image.ANTIALIAS)
            # Crop in the top, middle or bottom
            if crop_type == 'top':
                box = (0, 0, size[0], img.size[1])
            elif crop_type == 'middle':
                box = (int(round((img.size[0] - size[0]) / 2)), 0,
                       int(round((img.size[0] + size[0]) / 2)), img.size[1])
            elif crop_type == 'bottom':
                box = (img.size[0] - size[0], 0, img.size[0], img.size[1])
            else:
                raise ValueError('ERROR: invalid value for crop_type')
            img = img.crop(box)
        else:
            img = img.resize((size[0], size[1]),
                             Image.ANTIALIAS)
        # If the scale is the same, we do not need to crop
        img.save(modified_path)