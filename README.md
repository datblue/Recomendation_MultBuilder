ABOUT:
MultBuilder is used for building content with lda format by input a list of videoID in csv format

HOW TO RUN:
python2 main.py PATH_TO_VIDEO_ID_LIST PATH_TO_MULT_FILE PATH_TO_MAPPING_FILE_FROM_MULT_TO_VIDEOID PATH_TO_VOCAB_FILE

VIDEO_ID_LIST: a csv file contain only a column of ids without header

MULT_FILE: a file containing lda representations for videos

VOCAB_FILE: contain vocabularies used for lda represtation

MAPPING_FILE: a csv file mapping from a videoID to its lda represtation
