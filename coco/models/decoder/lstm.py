import torch
import torch.nn as nn

class LSTMDecoder(nn.Module):
    def __init__(
        self, tokenizer, embed_dim=512, hidden_size=512, out_embed_dim=512,
        num_layers=1, dropout_in=0.1, dropout_out=0.1,
    ):
        """
            LSTM hidden state has dimension: (num_layers*num_directions, batch_size, hidden_size)
            Because the image feature encoded by VGG has shape (batch_size, 512 channels), hidden_size
            must match 512 => LSTM(embed_dim, 512, num_layers)
        """
        super().__init__()
        # model params defined here
        self.tokenizer = tokenizer
        self.num_layers = num_layers
        vocab_size = self.tokenizer.vocab_size
        # TODO: load pretrained embedding or use train from scratch
        # Cannot use dropout when number of layer=1 because it only dropouts for all but last layer
        self.embed = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(
            embed_dim, 
            hidden_size, 
            num_layers,
            batch_first=True,
            # dropout=dropout_in
        ) 
        self.linear = nn.Linear(hidden_size, vocab_size)
        self.dropout = nn.Dropout(p=dropout_out)

    # def init_hidden(self, batch_size):
    #     return (torch.zeros(self.num_layers, batch_size, self.hidden_size), \
    #         torch.zeros(self.num_layers, batch_size, self.hidden_size))

    def forward(self, caption, image_feature):
        # embeddings = self.embed(caption)
        # # input_token = embeddings.permute(1,0,2)
        # bz, hidden_size = image_feature.size(0), image_feature.size(1)
        # c0 = image_feature.new_full(
        #     (self.num_layers, bz, hidden_size),
        #     0)
        # h0 = image_feature.unsqueeze(0) #  num_layer x batch_size x hidden_dim
        # output, (state, _) = self.lstm(embeddings, (h0, c0))

        caption = caption[:, :-1]
        embeddings = self.embed(caption)
        batch_size = image_feature.shape[0]
        image_feature = image_feature.unsqueeze(1)  # img_feat: [4,1,512], emb: [4, seqlen, 512]
        embeddings = torch.cat((image_feature, embeddings), 1)  # shape: [4, seqlen+1, 512]
        output, _ = self.lstm(embeddings)  # shape: [4, seqlen+1, vocab_size=2277]; h0 and c0 intialized to 0
        logits = self.dropout(self.linear(output)) # batch size x seqlen+1 x vocab size
        return logits


if __name__ == '__main__':
    # test decoder given encoder output
    import sys, os
    sys.path.append(os.path.abspath(os.path.join('../..', '')))
    sys.path.append('/Users/chenyuzhang/Desktop/JHU-6/DL/MICaptioning')

    from utils.tokenizer import Tokenizer
    from utils.dataset import ChestXrayDataSet, collate_fn
    from torchvision import transforms
    from models.encoder.encoder import EncoderCNN

    # caption_dir = '/mnt/d/Github/MICaptioning/iu_xray/iu_xray_captions.json'
    # data_dir = '/mnt/d/Github/MICaptioning/datasets'
    caption_dir = '//Users/chenyuzhang/Desktop/JHU-6/DL/MICaptioning/iu_xray/iu_xray_captions.json'
    data_dir = '/Users/chenyuzhang/Desktop/JHU-6/DL/MICaptioning/datasets'
    tokenizer = Tokenizer(caption_dir)
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize(256),
        transforms.RandomCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.Normalize((0.485, 0.456, 0.406),
                             (0.229, 0.224, 0.225))])

    train_dataset = ChestXrayDataSet(data_dir, 'train', tokenizer, transform)
    train_dataloader = torch.utils.data.DataLoader(dataset=train_dataset,
                                                   batch_size=4,
                                                   shuffle=False,
                                                   collate_fn=collate_fn)
    encoder = EncoderCNN()
    decoder = LSTMDecoder(tokenizer)
    # print(encoder)
    for img, caption, tags_vec in train_dataloader:
        # test encoding img into features
        _, encoder_out = encoder(img)
        decoder_out = decoder(caption, encoder_out)
        print(decoder_out.shape)
        break
