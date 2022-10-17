import os
# pip install shutil
import shutil


def move_function(base_path, images: dict, copy_images, percentage_test=0.3):
    num_test = int(len(images) * percentage_test)
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
        move(jpg, test_path, copy_images)
        move(images.get(jpg), test_path, copy_images)
        images.pop(jpg)

    for jpg in images.copy().keys():
        move(jpg, train_path, copy_images)
        move(images.get(jpg), train_path, copy_images)
        images.pop(jpg)
    
def move(initial_dir, final_dir, copy_images:bool):
    if copy_images == True:
        shutil.copy(initial_dir, final_dir)
    else:
        shutil.move(initial_dir, final_dir)

class ImageTestTrain:
    def __init__(self, base_path):
        self.base_path = base_path

    def move_images(self, folder_name=None, copy_images=False):
        for dir_name in os.listdir(self.base_path):
            images_path = dict()
            if dir_name == '.DS_Store':
                os.remove(os.path.join(self.base_path, dir_name))
                continue
            if len(dir_name) > 1:
                continue
            if folder_name is not None and dir_name != folder_name:
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
            move_function(self.base_path, images_path, copy_images)
        print('Done')

# Enter images folder path. Enter the full path and not relative path
path = r''
images_list = ImageTestTrain(path, copy_images=False)
images_list.move_images()
