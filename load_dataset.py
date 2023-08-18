import json
import random
from mcd.mcd_utils_test import get_mcd_splits, get_fewshot_splits

random.seed(2023) # control the randomness


def check_train(datum:dict, hold_combs:list) -> bool:
    '''
    return True: datum is supposed to be in train_set;
    otherwise: datum is supposed to be held out;
    '''
    for i in range(len(hold_combs)):
        for key in hold_combs[i].keys():
            if datum[key] != hold_combs[i][key]:
                return True
    return False

class ClsDataset():
    '''
    construct dataset(train // dev // test) for training and evaluating classifier.
    '''
    def __init__(self, file_path:str) -> None:
        fr = open(file_path, "r")
        cls_data = json.load(fr)
        random.shuffle(cls_data)
        '''
        [
            {
                'review':"...",
                'attr_1':"...",
                ...
                'attr_n':"..."
            }
        ]
        '''
        length = len(cls_data)
        # len(train) : len(test) : len(dev) = 7 : 1.5 : 1.5
        self.train_data = cls_data[:int(0.7 * length)]
        self.test_data = cls_data[int(0.7 * length) : int(0.85 * length)]
        self.dev_data = cls_data[int(0.85 * length):]

class GenDataset():
    '''
    construct train_set for training generator
    additionally return seen // unseen testing attribute combinations
    '''
    def __init__(self, file_path:str)->None:
        fr = open(file_path, "r")
        self.gen_data = json.load(fr)
        random.shuffle(self.gen_data)        
        '''
        [
            {
                'review':"...",
                'attr_1':"...",
                ...
                'attr_n':"..."
            }
        ]
        '''
        self.combs = list()
        self.attributes = dict()
        for datum in self.gen_data:
            comb = dict()
            for key in datum.keys():
                if key != 'review':
                    comb[key] = datum[key]

                    if key not in self.attributes:
                        self.attributes[key] = [datum[key]]
                    else:
                        if datum[key] not in self.attributes[key]:
                            self.attributes[key].append(datum[key])

            if comb not in self.combs:
                self.combs.append(comb)
        # self.combs = [comb1, comb2, ...]

    def create_train_by_combs(self, hold_combs:list)->None:
        '''
        e.g.,: hold_num = 1; hold_comb = [{'sentiment':'Pos', 'cuisine':'Mexican', ...}]
        e.g.,: hold_num = 2; hold_comb = [dict_1, dict_2] (dict_1 = {'sentiment':..., ...})
        '''
        self.train = list()
        for datum in self.gen_data:
            if check_train(datum, hold_combs) == True:
                self.train.append(datum)
        # attend: no need to construct test_set for open-domain controllable text generation

        self.unseen_combs = hold_combs 
        # test for composiitonal generalization
        self.seen_combs = [x for x in self.combs if x not in hold_combs] 
        # test for i.i.d. generalization
    
    
    def create_combs_mcd_splits(self, ratio=0.5, times=30000)->None:
        '''
        this function is to generate the splits of seen combinations || unseen combinations;
        then we can use the self.create_train_by_combs to generate the training set.
        '''
        _combs = list()
        keys = list(self.combs[0].keys())
        for comb in self.combs:
            string = ''
            for key in keys:
                # keep the same sequence
                if string == '':
                    string = comb[key]
                else:
                    string = string +' '+ comb[key]
            _combs.append(string)
        max_samples, rand_samples, min_samples = get_mcd_splits(_combs, ratio, times=times)
        def transform(inp_samples:list)->list:
            '''
            inp_samples =   list( 
                                tuple( 
                                    list_1( str1, str2,... ), 
                                    list_2( str1', str2',... ) 
                                    ) 
                                ...
                            )
            out_samples = list(
                                tuple( 
                                    list_1( dict1, dict2,... ), 
                                    list_2( dict1', dict2',... ) 
                                    ) 
                            )
            '''
            out_samples = list()

            for sample in inp_samples:
                seen, unseen = sample # both seen and unseen are lists
                _seen = list()
                _unseen = list()

                for comb in seen:
                    comb_li = comb.split(' ')
                    comb_dict = dict()
                    assert len(comb_li) == len(keys)
                    for i in range(len(keys)):
                        comb_dict[keys[i]] = comb_li[i]
                    _seen.append(comb)

                for comb in unseen:
                    comb_li = comb.split(' ')
                    comb_dict = dict()
                    assert len(comb_li) == len(keys)
                    for i in range(len(keys)):
                        comb_dict[keys[i]] = comb_li[i]
                    _unseen.append(comb)
                
                out_samples.append((_seen, _unseen))
            return out_samples
        # mcd_splits = [(seen_combs, unseen_combs),...]

        self.max_splits = transform(max_samples) # for maximum divergence (hard)
        self.rand_splits = transform(rand_samples) # for random divergence (normal)
        self.min_splits = transform(min_samples) # for minimum divergence (easy)

        pass

    def create_train_fewshot_split(self, shot_num=1)->None:
        '''
        basically, the fewshot_splits are constructed ** based ** on MCD splits;
        '''
        _combs = list()
        keys = list(self.combs[0].keys())
        for comb in self.combs:
            string = ''
            for key in keys:
                # keep the same sequence
                if string == '':
                    string = comb[key]
                else:
                    string = string +' '+ comb[key]
            _combs.append(string)
        
        max_attr_dim = 0
        for key in self.attributes:
            if len(self.attributes[key]) > max_attr_dim:
                max_attr_dim = len(self.attributes[key])
                
        max_samples, rand_samples, min_samples = get_fewshot_splits(_combs, max_attr_dim, shot_num)
        
        def transform(inp_samples:list)->list:
            '''
            inp_samples =   list( 
                                tuple( 
                                    list_1( str1, str2,... ), 
                                    list_2( str1', str2',... ) 
                                    ) 
                                ...
                            )
            out_samples = list(
                                tuple( 
                                    list_1( dict1, dict2,... ), 
                                    list_2( dict1', dict2',... ) 
                                    ) 
                            )
            '''
            out_samples = list()

            for sample in inp_samples:
                seen, unseen = sample # both seen and unseen are lists
                _seen = list()
                _unseen = list()

                for comb in seen:
                    comb_li = comb.split(' ')
                    comb_dict = dict()
                    assert len(comb_li) == len(keys)
                    for i in range(len(keys)):
                        comb_dict[keys[i]] = comb_li[i]
                    _seen.append(comb)

                for comb in unseen:
                    comb_li = comb.split(' ')
                    comb_dict = dict()
                    assert len(comb_li) == len(keys)
                    for i in range(len(keys)):
                        comb_dict[keys[i]] = comb_li[i]
                    _unseen.append(comb)
                
                out_samples.append((_seen, _unseen))
            return out_samples
        # mcd_splits = [(seen_combs, unseen_combs),...]

        self.fewshot_max_splits = transform(max_samples) # for maximum divergence (hard)
        self.fewshot_rand_splits = transform(rand_samples) # for random divergence (normal)
        self.fewshot_min_splits = transform(min_samples) # for minimum divergence (easy)
        pass



