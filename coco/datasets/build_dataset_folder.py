# build the train val test datasets
from pycocotools.coco import COCO
import os
import json
from shutil import copyfile

cwd = os.getcwd()

# train: 118287, val: 5000, test: 40670 (no annotations)

# create data folder
#for split in ['train', 'val', 'test']:
for split in ['val']:
    print(split)
    images_path = os.path.join(cwd, split+'2017')
    if split == 'test':
        annFile = '{}/annotations/image_info_test2017.json'.format(cwd)
    else:
        annFile = '{}/annotations/captions_{}.json'.format(cwd, split+'2017')
    coco_caps=COCO(annFile)

    index = 0
    split_path = os.path.join(cwd, split)
    if not os.path.exists(split_path):
        os.makedirs(split_path)

    _, _, filename = next(os.walk(images_path))
    for item in filename:
        folder = os.path.join(split_path, str(index))
        if not os.path.exists(folder):
            os.makedirs(folder)
        src = os.path.join(images_path, item)
        tgt_image = os.path.join(folder, 'image.png')
        copyfile(src, tgt_image)

        img_id = int(item.split('.')[0])
        #print(img_id)
        annIds = coco_caps.getAnnIds(imgIds=img_id)
        anns = coco_caps.loadAnns(annIds)[0]
        caption = anns['caption']
        with open(os.path.join(folder, 'caption.txt'), 'w') as f:
            f.write(caption)

        index += 1

