import os

os .system (". ./path.sh")
os .system ("python prepare_dict.py")
os .system ("sh local/swbd1_data_prep.sh dataset")
os .system ('utils/prepare_lang.sh data/dict "<unk>" data/local/lang_nosp data/lang_nosp')
os .system ("local/swbd1_train_lms.sh data/train/swbd/text data/dict/lexicon.txt data/lm")
os .system ('utils/format_lm_sri.sh --srilm-opts "-subset -prune-lowprobs -unk -tolower -order 3" data/lang_nosp data/lm/sw1.o3g.kn.gz data/local/dict_nosp/lexicon.txt data/lang_nosp_sw1_tg')
os .system ('steps/make_mfcc.sh --nj 50 data/train/swbd exp/make_mfcc/train/swbd mfcc')
os .system ("steps/compute_cmvn_stats.sh data/train/swbd exp/make_mfcc/train/swbd mfcc")
os .system ("utils/fix_data_dir.sh data/train/swbd")
os .system ("steps/train_mono.sh --nj 30 data/train/swbd data/lang_nosp exp/mono")