import os
from collections import Counter
from io import open
import sys
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

import config
import utils


class Mult_Builder:
    def __init__(self):
        self.vid_2_lda = []
        self.vectorizer = TfidfVectorizer(max_df=config.MAX_DF, min_df=config.MIN_DF)
        # self.vectorizer = TfidfVectorizer()

    def build_lda_content(self, contents):# contents is a dict {id: content}
        print ('BUILDING VOCAB ...')
        self.vectorizer.fit(contents.values())
        # self.vectorizer.fit(contents)
        vocab = self.vectorizer.vocabulary_
        sorted_vocab = sorted(vocab.iteritems(), key=lambda(k, v): (v, k))
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
                continue
            num_unique_word = unicode(len(bow))
            bow.insert(0, num_unique_word)
            lda_contents.append(u' '.join(bow))
            self.vid_2_lda.append([(len(lda_contents)-1), i])
        return lda_contents, sorted_vocab, self.vid_2_lda

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

    # contents_text = []
    # for k, v in contents.items():
    #     contents_text.append(v)
    # with open('contents.txt', 'w') as fw:
    #     text = u'\n'.join(contents_text)
    #     fw.write(text)

    print ('BUILDING CONTENT FINISHED')
    mb = Mult_Builder()
    mb.run(contents, mult_path, map_path, vocab_path)