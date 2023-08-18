'''
test the basic functions of the srcfile `load_dataset.py`
'''
from load_dataset import ClsDataset, GenDataset

cls_data = ClsDataset('/data2/home/zhaoyi/compctg/dataset/Fyelp-v4/cls.json')
gen_data = GenDataset('/data2/home/zhaoyi/compctg/dataset/Fyelp-v4/gen.json')

gen_data.create_combs_mcd_splits(0.5, 300) # test for mcd splits
gen_data.create_train_fewshot_split(1) # test for few-shot splits