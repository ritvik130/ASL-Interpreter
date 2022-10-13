import os
# pip install shutil
import shutil


def move_function(base_path, images: dict):
    num_test = int(len(images) * 0.3)
    test_path = None
    train_path = None
    for directory in os.listdir(base_path):
        if directory == 'test':
            test_path = os.path.join(base_path, directory)
        if directory == 'train':
            train_path = os.path.join(base_path, directory)

    if test_path is None or train_path is None:
        print("Error, test/train path not set")
        exit(0)

    for jpg in images.copy().keys():
        num_test -= 1
        if num_test <= 0:
            break
        shutil.move(jpg, test_path)
        shutil.move(images.get(jpg), test_path)
        images.pop(jpg)

    for jpg in images.copy().keys():
        shutil.move(jpg, train_path)
        shutil.move(images.get(jpg), train_path)
        images.pop(jpg)


class ImageTestTrain:
    def __init__(self, base_path):
        self.base_path = base_path

    def move_images(self):
        for dir_name in os.listdir(self.base_path):
            images_path = dict()
            if dir_name == '.DS_Store':
                os.remove(os.path.join(self.base_path, dir_name))
                continue
            if len(dir_name) > 1:
                continue
            dir_path = os.path.join(self.base_path, dir_name)
            for item in os.listdir(dir_path):
                name, _ = os.path.splitext((os.path.basename(item)))
                if name == '.DS_Store':
                    os.remove(os.path.join(dir_path, name))
                elif os.path.exists(f'{os.path.join(dir_path, name)}.jpg') and os.path.exists(
                                    f'{os.path.join(dir_path, name)}.xml'):
                    images_path[f'{os.path.join(dir_path, name)}.jpg'] = f'{os.path.join(dir_path, name)}.xml'
                else:
                    print(f"Error!! Skipping file: {name}")
            move_function(self.base_path, images_path)
        print('Done')

# Enter images folder path. Enter the full path and not relative path
path = r''
images_list = ImageTestTrain(path)
images_list.move_images()
