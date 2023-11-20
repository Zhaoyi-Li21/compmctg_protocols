'''
test the basic functions of the srcfile `load_dataset.py`
'''
from load_dataset import ClsDataset, GenDataset

cls_data = ClsDataset('/data2/home/zhaoyi/compctg/dataset/Fyelp-v4/cls.json')
gen_data = GenDataset('/data2/home/zhaoyi/compctg/dataset/Fyelp-v4/gen.json')

# gen_data.create_combs_mcd_splits(0.5, 3000) # test for mcd splits
# print(gen_data.max_splits[0])
# print(len(gen_data.max_splits))
# print(len(gen_data.min_splits))
# print(len(gen_data.rand_splits))

# gen_data.create_train_fewshot_split(1) # test for few-shot splits

min_div = 0.0
max_div = 0.335
eta = 0.75

set_div = (max_div-min_div) * eta + min_div
print(set_div)
gen_data.create_specific_divergence_splits(set_div, torlerate=0.1, times=3000)
print(gen_data.div_splits[0])
print(len(gen_data.div_splits))

# hold_outs = gen_data.max_splits[0][1] # unseen
hold_outs = gen_data.div_splits[0][1] # unseen
print(len(hold_outs))
gen_data.create_train_by_combs(hold_outs)
print(len(gen_data.train))
print(gen_data.unseen_combs)
print(len(gen_data.unseen_combs))
print(len(gen_data.gen_data))

