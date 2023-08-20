'''
test the basic functions of the srcfile `load_dataset.py`
'''
from load_dataset import ClsDataset, GenDataset

cls_data = ClsDataset('/data2/home/zhaoyi/compctg/dataset/Fyelp-v4/cls.json')
gen_data = GenDataset('/data2/home/zhaoyi/compctg/dataset/Fyelp-v4/gen.json')

gen_data.create_combs_mcd_splits(0.5, 300) # test for mcd splits
print(gen_data.max_splits[0])
print(len(gen_data.max_splits))
print(len(gen_data.min_splits))
print(len(gen_data.rand_splits))
# gen_data.create_train_fewshot_split(1) # test for few-shot splits
hold_outs = gen_data.max_splits[0][1] # unseen
print(len(hold_outs))
gen_data.create_train_by_combs(hold_outs)
print(len(gen_data.train))
print(gen_data.unseen_combs)
print(len(gen_data.unseen_combs))
print(len(gen_data.gen_data))
