'''
test the basic functions of the srcfile `load_dataset.py`
'''
from load_dataset import ClsDataset, GenDataset

dataset = "Fyelp-v1" # eta = 0.25, 0.5, 0.75
# dataset = "Fyelp-v3" # eta = 0.25, 0.5, 0.75
# dataset = "Yelp" # eta = 0.65 only

cls_data = ClsDataset('/data2/home/zhaoyi/compctg/dataset/'+dataset+'/cls.json')
gen_data = GenDataset('/data2/home/zhaoyi/compctg/dataset/'+dataset+'/gen.json')

gen_data.create_combs_mcd_splits(0.5, 10000) # test for mcd splits
print(gen_data.max_splits[0])
print(len(gen_data.max_splits))
print(len(gen_data.min_splits))
print(len(gen_data.rand_splits))

# gen_data.create_train_fewshot_split(1) # test for few-shot splits

# min_div = 0.0
# max_div = 0.335
# eta = 0.75

def div_splits(dataset="Fyelp-v3", eta=0.25, tor=0.1):
    # or dataset =  "Yelp"
    # eta = {0.25, 0.5, 0.75} 
    if dataset == "Fyelp-v3":
        max_div = 0.331
        min_div = 0.0
    elif dataset == "Yelp":
        max_div = 0.5
        min_div = 0.0
    elif dataset == "Fyelp-v1":
        max_div = 0.512
        min_div = 0.002
    else:
        raise Exception("dataset is invalid!")
    set_div = (max_div-min_div) * eta + min_div
    
    gen_data.create_specific_divergence_splits(set_div, torlerate=tor, times=100000)
    print(gen_data.div_splits[0])
    print(len(gen_data.div_splits))
    
    hold_outs = gen_data.div_splits[0][1]
    
    
    gen_data.create_train_by_combs(hold_outs)
    print(len(gen_data.train))
    print(gen_data.unseen_combs)
    print(len(gen_data.unseen_combs))
    print(len(gen_data.gen_data))



# hold_outs = gen_data.max_splits[0][1] # unseen
# hold_outs = gen_data.div_splits[0][1] # unseen

# print(len(hold_outs))
# gen_data.create_train_by_combs(hold_outs)
# print(len(gen_data.train))
# print(gen_data.unseen_combs)
# print(len(gen_data.unseen_combs))
# print(len(gen_data.gen_data))



'''
e.g., usage of div_splits():
'''
div_splits(dataset=dataset, eta=0.65, tor=0.1)

