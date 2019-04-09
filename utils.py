import psycopg2
import unicodedata

from pycparser.c_ast import ID

import config
import pandas as pd
from regex import regex
# from tokenizer.tokenizer import Tokenizer

regexer = regex()
# tokenizer = Tokenizer()

def hierachy_dict(corpus):
    eng_vocab = {}
    for w,idx in corpus.items():
        w = w.lower()
        c = w[0]
        try:
            eng_vocab[c][len(w)].update({w : idx})
        except:
            try:
                eng_vocab[c].update({len(w) : {w : idx}})
            except:
                eng_vocab.update({c : {len(w) : {w : idx}}})
    return eng_vocab

def process_content(video_df):
    contents = {}
    for _, row in video_df.iterrows():
        id = row['id']
        name = unicode(row['name'], encoding='utf-8')
        name = unicodedata.normalize('NFKC', name.strip())
        name = u' '.join(name.split())
        try:
            des = unicode(row['description'], encoding='utf-8')
            des = unicodedata.normalize('NFKC', des.strip())
            des = u' '.join(des.split())
        except:
            des = name
        if len(des) == 0:
            des = name
        try:
            tag = unicode(row['tag'], encoding='utf-8')
            tag = unicodedata.normalize('NFKC', tag.strip())
            tag = u' '.join(tag.split())
        except:
            tag = name
        if len(tag) == 0:
            tag = name
        full_text = u'\n'.join([name, des, tag]).lower()
        text = full_text.replace(u'_', u'')
        # text = tokenizer.predict(text)
        text = u' '.join(regexer.run_regex(text).split())
        # text = text.replace(u'\n', u' ')
        if len(text) == 0:
            print (full_text)
            continue
        contents.update({id: text})
    # print ('Number of contents: %d ' % (len(contents)))
    return contents


def connect_db():
    print ('CONNECTING SERVER ...')
    connection = psycopg2.connect(user=config.POSTGRE_USER,
                                  password=config.POSTGRE_PWD,
                                  host=config.POSTGRE_HOST,
                                  port=config.POSTGRE_PORT,
                                  database=config.POSTGRE_DB)
    cursor = connection.cursor()
    return cursor

def build_video_content(videoID_list_path):
    print ('START BUILDING VIDEO CONTENTS')
    ID_list_df = pd.read_csv(videoID_list_path, header=None)
    ID_list_df.columns = ['id']
    print ('THERE ARE %d VIDEOS IN VIDEO LIST' % (ID_list_df['id'].count()))

    cursor = connect_db()
    # posgreSQL_query = 'SELECT id, name, description, tag FROM video_full WHERE id IN (2173837, 00000)'
    # cursor.execute("""select * from INFORMATION_SCHEMA.COLUMNS where table_name = 'video_full' """)
    # for col in cursor.fetchall():
    #     print(col)
    print ('DOING QUERY FOR VIDEO DATA ...')
    posgreSQL_query = 'SELECT id, name, description, tag FROM video_full WHERE is_active=1 AND status=2'
    cursor.execute(posgreSQL_query)
    videos = cursor.fetchall()

    videos_df = pd.DataFrame(videos, columns=['id', 'name', 'description', 'tag'])

    # for record in cursor.fetchall():
    #     print record[0]

    print ('MERGING VIDEOID LIST WITH VIDEOS DATA ...')
    df = pd.merge(videos_df, ID_list_df, on='id')
    print ('THERE ARE %d VIDEOS IN VIDEO LIST EXIST IN DATABASE' % (df['id'].count()))
    print ('PROCESSING VIDEO CONTENTS ...')
    contents = process_content(df)
    print ('BUILDING CONTENT FINISHED')
    print ('THERE ARE %d VIDEOS HAVE CONTENTS' % (len(contents.items())))
    return contents

if __name__ == '__main__':
    videoID_list_path = '../data/videos.dat'
    contents = build_video_content(videoID_list_path)
    for k,v in contents.items():
        print v
