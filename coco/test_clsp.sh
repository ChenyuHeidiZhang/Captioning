WORK_DIR=/export/b02/czhan105/coco
TRAIN=$WORK_DIR/train.py
DATA=/export/b02/czhan105/coco/datasets
CHECKPOINT_FOLDER=/export/b02/czhan105/coco/checkpoints
CAPTION=/export/b02/czhan105/coco/datasets/annotations/captions_train2017.json

python $TRAIN \
    --mode test --cpu \
    --caption-dir $CAPTION \
    --data-dir $DATA \
    --max-epoch 10 \
    --load-dir $CHECKPOINT_FOLDER/checkpoint0.pt \
    --arch transformer
