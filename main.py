from collections import Counter
from io import open
import sys
import pandas as pd

import config
import utils


class Mult_Builder:
    def __init__(self):
        self.vid_2_lda = []

    def build_vocab(self, contents):
        vocab_set = set(u' '.join(contents.values()).split())
        vocab = {}
        for k, v in enumerate(vocab_set):
            vocab.update({v: k})
        return vocab

    def build_lda_content(self, contents):# contents is a dict {id: content}
        print ('BUILDING VOCAB ...')
        vocab = self.build_vocab(contents)
        h_dict = utils.hierachy_dict(vocab)
        lda_contents = []
        print ('BUILDING LDA ...')
        for i, content in contents.items():
            c = Counter(content.split())
            bow = []
            for word, freq in c.items():
                try:
                    idx = h_dict[word[0]][len(word)][word]
                    s = u':'.join([unicode(idx), unicode(freq)])
                    bow.append(s)
                except:
                    continue
            if len(bow) == 0:
                print content
                continue
            num_unique_word = unicode(len(bow))
            bow.insert(0, num_unique_word)
            lda_contents.append(u' '.join(bow))
            self.vid_2_lda.append([(len(lda_contents)-1), i])
        print ('BUILDING LDA FINISHED, THERE ARE %d LDA' % (len(self.vid_2_lda)))
        return lda_contents, vocab, self.vid_2_lda

    def run(self, contents, mult_path, map_path, vocab_path):
        self.lda_contents, self.vocab, self.vid_2_lda = self.build_lda_content(contents)
        print ('SAVING MODELS ...')
        lda_contents = u'\n'.join(self.lda_contents)
        with open(mult_path, 'w') as fw:
            fw.write(lda_contents)
        with open(vocab_path, 'w', encoding='utf-8') as fw:
            for w in self.vocab:
                fw.write(w[0] + '\n')
        df = pd.DataFrame(self.vid_2_lda, columns=['id', 'video_id'])
        df.to_csv(map_path, index=False)


if __name__ == '__main__':
    if (len(sys.argv) != 5):
       print 'usage: python main.py [path_to_videoIDs] [path_to_mult] [path_to_map_mult_2_video] [path_to_vocab] \n'
       sys.exit(1)
    videoID_list_path = sys.argv[1]
    mult_path = sys.argv[2]
    map_path = sys.argv[3]
    vocab_path = sys.argv[4]

    contents = utils.build_video_content(videoID_list_path)

    mb = Mult_Builder()
    mb.run(contents, mult_path, map_path, vocab_path)
