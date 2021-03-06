# tokenizer for captions

import torch
import os
import json
import numpy as np
from collections import Counter
from string import punctuation
from pycocotools.coco import COCO
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
# nltk.download('punkt') # if not installed on your local, do this for tokenizer to work
# TODO: maybe use pickle to save the vocab to speed up the time


class Tokenizer():
    # Load datasets, also create vocab for tokenizer
    def __init__(self, caption_dir, MIN_FREQ=2, RM_TOP=0):
        # caption_dir: captions_train2017.json
        coco_caps=COCO(caption_dir)
        annIds = coco_caps.getAnnIds()  # get all ids
        anns = coco_caps.loadAnns(annIds)
        print(len(anns))

        text = ' '.join([ann['caption'] for ann in anns])
        sentences = self.tokenize(text)
        vocab = [tokens for sent in sentences for tokens in sent]
        vocab_counts = Counter(vocab)
        stopwords = set([s[0] for s in vocab_counts.most_common(RM_TOP)])
        self.vocab = set([v for v in set(vocab) if vocab_counts[v] >= MIN_FREQ and v not in stopwords] + 
            ['<bos>'] + ['<eos>'] + ['<pad>'] + ['<unk>'])

        self.vocab_size = len(self.vocab)
        print('vocab_size:', self.vocab_size)
        vocab_file = 
        self.w2i = {w: i for i, w in enumerate(sorted(self.vocab))}
        self.i2w = {i: w for i, w in enumerate(sorted(self.vocab))}
        self.bos = self.w2i['<bos>']
        self.eos = self.w2i['<eos>']
        self.pad = self.w2i['<pad>']
        self.unk = self.w2i['<unk>']

    def encode(self, input_text):
        """ encode the input using established vocab and dictionary """
        sentences = self.tokenize(input_text)
        output = [self.bos]
        for sent in sentences:
            for tokens in sent:
                if tokens not in self.w2i:
                    output.append(self.unk)
                else:
                    output.append(self.w2i[tokens])
        output.append(self.eos)
        return output

    def decode(self, input_token):
        """ decode the input token (in batch) into words """
        bz, seqlen = input_token.size(0), input_token.size(0)
        token = input_token.tolist()
        output = []
        for i in range(bz):
            # strip padding and unknown tokens to avoid BLEU score buffed
            sent = " ".join([self.i2w[t] for t in token[i] if t != self.pad and t != self.unk])
            output.append(sent)
        return output

    def tokenize(self, text):
        """
        Simple tokenizer (sentences and then words)
        """
        sentences = sent_tokenize(text)
        examples = []
        for sentence in sentences:
            sentence = "".join(char for char in sentence if char not in punctuation)
            sentence = "".join(char for char in sentence if not char.isdigit())
            sentence = sentence.lower()
            tokens = word_tokenize(sentence)
            examples.append(tokens)
        return examples



if __name__ == '__main__':  
    # test tokenizer
    #caption_dir = '/mnt/d/Github/MICaptioning/iu_xray/iu_xray_captions.json'
    caption_dir = '/Users/chenyuzhang/Desktop/JHU-6/DL/annotations/captions_val2017.json'
    tokenizer = Tokenizer(caption_dir)
    # text = """
    # COPD and chronic opacities more pronounced in the lower lung XXXX. 
    # There is persistent mild elevation right hemidiaphragm. 
    # There is suggestion of subtle patchy opacities in lower lung XXXX bilaterally. 
    # This is XXXX to be similar to XXXX scan. The heart is normal. 
    # The aorta is calcified and tortuous. The skeletal structures show scoliosis and arthritic changes."""
    # token = tokenizer.encode(text)
    # decode_out = tokenizer.decode(token)
    # print(token)
    # print(decode_out)
    


