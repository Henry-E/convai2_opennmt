path_to_data=~/convai2_opennmt
path_to_opennmt=~/OpenNMT-py
python $path_to_opennmt/preprocess.py -src_seq_length 150 -tgt_seq_length 100 -dynamic_dict -share_vocab -src_vocab_size 15000 -tgt_vocab_size 15000 -save_data $path_to_data/processed -train_src $path_to_data/train_self_original_no_cands_source.txt -train_tgt $path_to_data/train_self_original_no_cands_target.txt -valid_src $path_to_data/valid_self_original_no_cands_source.txt -valid_tgt $path_to_data/valid_self_original_no_cands_target.txt
python $path_to_opennmt/train.py -gpuid 0 -train_steps 2400000 -data $path_to_data/processed -save_model $path_to_data/model -layers 1 -word_vec_size 300 -share_embeddings -rnn_size 300 -copy_attn -copy_attn_force
model=$(for i in $path_to_data/model*; do printf '%s\n' "$i"; break; done)
python $path_to_opennmt/translate.py -model $model -src $path_to_data/valid_self_original_no_cands_source.txt -gpu 0 -beam_size 30 -output $path_to_data/generated_output -n_best 1
