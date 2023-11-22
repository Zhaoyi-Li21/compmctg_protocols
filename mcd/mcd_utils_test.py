# coding=utf-8
# Copyright 2018 The Google AI Language Team Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for mcd_utils."""

import mcd.mcd_utils as mcd_utils # use from outer file
# import mcd_utils # direct usage


import random
random.seed(2023)
# random.seed(1)
# Define unigrams as atoms for tests.
def _get_atoms_fn(example):
  return set(example.split())

'''
# Define bigrams as compounds for tests.
def _get_compounds_fn(example):
  tokens = example.split()
  bigrams = set()
  for idx in range(len(tokens) - 1):
    bigrams.add(" ".join(tokens[idx:idx + 2]))
  return bigrams
'''
def _get_compounds_fn(example):
  tokens = example.split()
  co_occurs = set()
  for i in range(len(tokens)):
    for j in range(i+1, len(tokens)):
      if tokens[i] != tokens[j]:        
        co_occurs.add(" ".join([tokens[i], tokens[j]]))
  return co_occurs

def get_mcd_splits(combs, ratio=0.5, rand_sample_cnt=10, 
                   max_sample_cnt=10, min_sample_cnt=10,
                   round_=3, times=30000):
    '''
    combs = ["a1 b1 c1", ....]
    '''
    
    #examples_in_1 = ["a1 b1 c1", "a2 b2 c2", "a2 b1 c2", "a1 b2 c2"]
    #examples_in_2 = ["a2 b1 c1", "a2 b2 c1", "a1 b2 c1", "a1 b1 c2"]

    #examples_in_1 = ["a1 b1 c1", "a2 b2 c2", "a2 b1 c2", "a2 b1 c1", "a3 b1 c1", "a3 b2 c2"]
    #examples_in_2 = ["a1 b2 c2", "a2 b2 c1", "a1 b2 c1", "a1 b1 c2", "a3 b1 c2", "a3 b2 c1"]


    max_divergence = -0.1
    min_divergence = 1.1
    div_sum = 0.
    
    cnt = 0
    
    rand_samples = list()
    max_samples = list()
    min_samples = list()

    for i in range(times):
      if i%2000 == 0: print('sample number: --- ', i)
      examples_in_1 = random.sample(combs, int(len(combs) * ratio))
      # examples_in_1 = random.sample(tot, 5)
      # examples_in_1 = random.sample(tot, int(len(tot)-1))
      examples_in_2 = list(set(combs) - set(examples_in_1))
      #examples_in_1, examples_in_2 = mcd_utils.balance_atoms(examples_in_1, examples_in_2, _get_atoms_fn, 1000, 1)


      atoms_2 = set()
      atoms_1 = set()
      for example in examples_in_1:
        atoms_1 = atoms_1.union(_get_atoms_fn(example))
      for example in examples_in_2:
        atoms_2 = atoms_2.union(_get_atoms_fn(example))
      
      flag_1 = False
      flag_2 = False
      
      for example in examples_in_1:
        for atom in _get_atoms_fn(example):
          if atom not in atoms_2:
            flag_1 = True
      if flag_1 == True: continue

      for example in examples_in_2:
        for atom in _get_atoms_fn(example):
          if atom not in atoms_1:
            flag_2 = True
      if flag_2 == True: continue
      # break

      if len(rand_samples) < rand_sample_cnt:
        if (examples_in_1, examples_in_2) not in rand_samples:
          rand_samples.append((examples_in_1, examples_in_2))

      compound_divergence_in = mcd_utils.measure_example_divergence(
          examples_in_1, examples_in_2, _get_compounds_fn)
      #self.assertEqual(compound_divergence_in, 0.8)
      # print(compound_divergence_in)
      div_sum += compound_divergence_in
      cnt += 1
      examples_out_1, examples_out_2 = mcd_utils.swap_examples(
          examples_in_1, examples_in_2, _get_compounds_fn, _get_atoms_fn, 
          print_frequencies=False,direction='max')

      # print(examples_out_1, examples_out_2)
      compound_divergence_out = mcd_utils.measure_example_divergence(
          examples_out_1, examples_out_2, _get_compounds_fn)
      # print(compound_divergence_out)

      r_examples_out_1, r_examples_out_2 = mcd_utils.swap_examples(
          examples_in_1, examples_in_2, _get_compounds_fn, _get_atoms_fn, 
          print_frequencies=False,direction='min')
      
      r_compound_divergence_out = mcd_utils.measure_example_divergence(
          r_examples_out_1, r_examples_out_2, _get_compounds_fn)
      
      #rounding
      compound_divergence_out = round(compound_divergence_out, round_)
      r_compound_divergence_out = round(r_compound_divergence_out, round_)

      if compound_divergence_out > max_divergence:
        max_divergence = compound_divergence_out
        e1 = examples_out_1
        e2 = examples_out_2
        maxs = {'-'.join(e1)}
        max_samples = [(e1, e2)]

      elif compound_divergence_out == max_divergence:
        e1 = examples_out_1
        e2 = examples_out_2
        maxs.add('-'.join(e1))
        if len(max_samples) < max_sample_cnt:
          if (e1, e2) not in max_samples:
            max_samples.append((e1, e2))
        
      if r_compound_divergence_out < min_divergence:
        min_divergence = r_compound_divergence_out
        e1 = r_examples_out_1
        e2 = r_examples_out_2
        mins = {'-'.join(e1)}
        min_samples = [(e1, e2)]

      elif r_compound_divergence_out == min_divergence:
        e1 = r_examples_out_1
        e2 = r_examples_out_2
        mins.add('-'.join(e1))
        if len(min_samples) < min_sample_cnt:
          if (e1, e2) not in min_samples:
            min_samples.append((e1, e2))

    print('when constructing MCD splits', round(div_sum/cnt,round_), max_divergence, len(maxs), min_divergence, len(mins))
    return max_samples, rand_samples, min_samples

def get_div_splits(combs, div=0, torlerate=0.1, sample_num=10, ratio=0.5, round_=3, times=30000):
    '''
    combs = ["a1 b1 c1", ....]
    div = (max-min)*\eta + min; where \eta = 0, 0.25, 0.5, 0.75, 1
    '''

    div_sum = 0.
    
    cnt = 0
    
    total_div = 0.

    tgt_samples = list()
    tgts = set()

    for i in range(times):
      if i%2000 == 0: print('sample number: --- ', i)
      examples_in_1 = random.sample(combs, int(len(combs) * ratio))
      # examples_in_1 = random.sample(tot, 5)
      # examples_in_1 = random.sample(tot, int(len(tot)-1))
      examples_in_2 = list(set(combs) - set(examples_in_1))
      #examples_in_1, examples_in_2 = mcd_utils.balance_atoms(examples_in_1, examples_in_2, _get_atoms_fn, 1000, 1)


      atoms_2 = set()
      atoms_1 = set()
      for example in examples_in_1:
        atoms_1 = atoms_1.union(_get_atoms_fn(example))
      for example in examples_in_2:
        atoms_2 = atoms_2.union(_get_atoms_fn(example))
      
      flag_1 = False
      flag_2 = False
      
      for example in examples_in_1:
        for atom in _get_atoms_fn(example):
          if atom not in atoms_2:
            flag_1 = True
      if flag_1 == True: continue

      for example in examples_in_2:
        for atom in _get_atoms_fn(example):
          if atom not in atoms_1:
            flag_2 = True
      if flag_2 == True: continue
      # break



      compound_divergence_in = mcd_utils.measure_example_divergence(
          examples_in_1, examples_in_2, _get_compounds_fn)
      #self.assertEqual(compound_divergence_in, 0.8)
      # print(compound_divergence_in)
      div_sum += compound_divergence_in
      cnt += 1

      examples_out_1, examples_out_2 = mcd_utils.swap_examples(
          examples_in_1, examples_in_2, _get_compounds_fn, _get_atoms_fn, 
          print_frequencies=False, direction='set_div', set_div= div,threshold=torlerate)

      # print(examples_out_1, examples_out_2)
      compound_divergence_out = mcd_utils.measure_example_divergence(
          examples_out_1, examples_out_2, _get_compounds_fn)
      # print(compound_divergence_out)

      #rounding
      compound_divergence_out = round(compound_divergence_out, round_)


      if compound_divergence_out > div * (1-torlerate) and compound_divergence_out < div * (1+torlerate):
        e1 = examples_out_1
        e2 = examples_out_2
        if '-'.join(e1) not in tgts:
          tgts.add('-'.join(e1))
          if (e1, e2) not in tgt_samples:
            total_div += compound_divergence_out
            tgt_samples.append((e1, e2))

      if len(tgts) >= sample_num:
        break

    print('when constructing divergence splits, random divergence = ', round(div_sum/cnt,round_),'sampled divergence = ', round(total_div/len(tgt_samples), round_), len(tgts), len(tgt_samples))
    return tgt_samples

def get_fewshot_splits(combs, max_attribute_dim, shot=1, rand_sample_cnt=10, 
                   max_sample_cnt=10, min_sample_cnt=10,
                   round_=2, times=30000):
    '''
    combs = ["a1 b1 c1", ....]
    '''
    
    #examples_in_1 = ["a1 b1 c1", "a2 b2 c2", "a2 b1 c2", "a1 b2 c2"]
    #examples_in_2 = ["a2 b1 c1", "a2 b2 c1", "a1 b2 c1", "a1 b1 c2"]

    #examples_in_1 = ["a1 b1 c1", "a2 b2 c2", "a2 b1 c2", "a2 b1 c1", "a3 b1 c1", "a3 b2 c2"]
    #examples_in_2 = ["a1 b2 c2", "a2 b2 c1", "a1 b2 c1", "a1 b1 c2", "a3 b1 c2", "a3 b2 c1"]


    max_divergence = -0.1
    min_divergence = 1.1
    div_sum = 0.
    
    cnt = 0
    
    rand_samples = list()
    max_samples = list()
    min_samples = list()

    for i in range(times):
      if i%2000 == 0: print('sample number: --- ', i)
      examples_in_1 = random.sample(combs, int(shot*max_attribute_dim))
      # examples_in_1 = random.sample(tot, 5)
      # examples_in_1 = random.sample(tot, int(len(tot)-1))
      examples_in_2 = list(set(combs) - set(examples_in_1))
      #examples_in_1, examples_in_2 = mcd_utils.balance_atoms(examples_in_1, examples_in_2, _get_atoms_fn, 1000, 1)

      atoms_2 = set()
      atoms_1 = set()
      for example in examples_in_1:
        atoms_1 = atoms_1.union(_get_atoms_fn(example))
      for example in examples_in_2:
        atoms_2 = atoms_2.union(_get_atoms_fn(example))
      
      flag_1 = False
      flag_2 = False
      
      for example in examples_in_1:
        for atom in _get_atoms_fn(example):
          if atom not in atoms_2:
            flag_1 = True
      if flag_1 == True: continue

      for example in examples_in_2:
        for atom in _get_atoms_fn(example):
          if atom not in atoms_1:
            flag_2 = True
      if flag_2 == True: continue
      # break

      if len(rand_samples) < rand_sample_cnt:
        if (examples_in_1, examples_in_2) not in rand_samples:
          rand_samples.append((examples_in_1, examples_in_2))

      compound_divergence_in = mcd_utils.measure_example_divergence(
          examples_in_1, examples_in_2, _get_compounds_fn)
      #self.assertEqual(compound_divergence_in, 0.8)
      # print(compound_divergence_in)
      div_sum += compound_divergence_in
      cnt += 1
      examples_out_1, examples_out_2 = mcd_utils.swap_examples(
          examples_in_1, examples_in_2, _get_compounds_fn, _get_atoms_fn, 
          print_frequencies=False,direction='max')

      # print(examples_out_1, examples_out_2)
      compound_divergence_out = mcd_utils.measure_example_divergence(
          examples_out_1, examples_out_2, _get_compounds_fn)
      # print(compound_divergence_out)

      r_examples_out_1, r_examples_out_2 = mcd_utils.swap_examples(
          examples_in_1, examples_in_2, _get_compounds_fn, _get_atoms_fn, 
          print_frequencies=False,direction='min')
      
      r_compound_divergence_out = mcd_utils.measure_example_divergence(
          r_examples_out_1, r_examples_out_2, _get_compounds_fn)
      
      #rounding
      compound_divergence_out = round(compound_divergence_out, round_)
      r_compound_divergence_out = round(r_compound_divergence_out, round_)

      if compound_divergence_out > max_divergence:
        max_divergence = compound_divergence_out
        e1 = examples_out_1
        e2 = examples_out_2
        maxs = {'-'.join(e1)}
        max_samples = [(e1, e2)]

      elif compound_divergence_out == max_divergence:
        e1 = examples_out_1
        e2 = examples_out_2
        maxs.add('-'.join(e1))
        if len(max_samples) < max_sample_cnt:
          if (e1, e2) not in max_samples:
            max_samples.append((e1, e2))
        
      if r_compound_divergence_out < min_divergence:
        min_divergence = r_compound_divergence_out
        e1 = r_examples_out_1
        e2 = r_examples_out_2
        mins = {'-'.join(e1)}
        min_samples = [(e1, e2)]

      elif r_compound_divergence_out == min_divergence:
        e1 = r_examples_out_1
        e2 = r_examples_out_2
        mins.add('-'.join(e1))
        if len(min_samples) < min_sample_cnt:
          if (e1, e2) not in min_samples:
            min_samples.append((e1, e2))

    print('when constructing MCD splits', round(div_sum/cnt,round_), max_divergence, len(maxs), min_divergence, len(mins))
    return max_samples, rand_samples, min_samples

# class McdUtilsTest(tf.test.TestCase):
class McdUtilsTest():
  '''
  def test_divergence_is_0(self):
    examples_1 = ["jump twice", "walk thrice"]
    examples_2 = ["jump twice", "walk thrice"]
    compound_divergence = mcd_utils.measure_example_divergence(
        examples_1, examples_2, _get_compounds_fn)
    self.assertEqual(compound_divergence, 0.0)

  def test_divergence_is_1(self):
    examples_1 = ["jump thrice", "walk twice"]
    examples_2 = ["jump twice", "walk thrice"]
    compound_divergence = mcd_utils.measure_example_divergence(
        examples_1, examples_2, _get_compounds_fn)
    self.assertEqual(compound_divergence, 1.0)
  '''
  
  def test_swap_examples(self):
    print("my test start")
    #examples_in_1 = ["a1 b1 c1", "a2 b2 c2", "a2 b1 c2", "a1 b2 c2"]
    #examples_in_2 = ["a2 b1 c1", "a2 b2 c1", "a1 b2 c1", "a1 b1 c2"]

    #examples_in_1 = ["a1 b1 c1", "a2 b2 c2", "a2 b1 c2", "a2 b1 c1", "a3 b1 c1", "a3 b2 c2"]
    #examples_in_2 = ["a1 b2 c2", "a2 b2 c1", "a1 b2 c1", "a1 b1 c2", "a3 b1 c2", "a3 b2 c1"]

    tot = list()
    for a in ['a1', 'a2']:
      for b in ['b1', 'b2']:
      # for b in ['b1', 'b2', 'b3', 'b4', 'b5']:
      # for b in ['b1', 'b2', 'b3']:
        #for c in ['c1', 'c2', 'c3']:
        for c in ['c1', 'c2']:
        #for c in ['c1', 'c2', 'c3', 'c4', 'c5']:
          #for d in ['d1', 'd2']:
          #for d in ['d1', 'd2', 'd3', 'd4', 'd5']:
            #for e in ['e1', 'e2']:
              #tot.append(a+' '+b+' '+c+' '+d+' '+e)
              tot.append(a+' '+b+' '+c)
              #tot.append(a+' '+b)
    max_divergence = -0.1
    min_divergence = 1.1
    rand_sample_cnt=10
    max_sample_cnt=10 
    min_sample_cnt=10
    div_sum = 0.
    times = 3000
    cnt = 0
    for i in range(times):
      if i%1000 == 0: print(i)
      examples_in_1 = random.sample(tot, int(len(tot)*0.5))
      #examples_in_1 = random.sample(tot, 5)
      # examples_in_1 = random.sample(tot, int(len(tot)-1))
      examples_in_2 = list(set(tot) - set(examples_in_1))
      #examples_in_1, examples_in_2 = mcd_utils.balance_atoms(examples_in_1, examples_in_2, _get_atoms_fn, 1000, 1)
      
      atoms_2 = set()
      atoms_1 = set()
      for example in examples_in_1:
        atoms_1 = atoms_1.union(_get_atoms_fn(example))
      for example in examples_in_2:
        atoms_2 = atoms_2.union(_get_atoms_fn(example))
      
      flag_1 = False
      flag_2 = False
      
      for example in examples_in_1:
        for atom in _get_atoms_fn(example):
          if atom not in atoms_2:
            flag_1 = True
      if flag_1 == True: continue

      for example in examples_in_2:
        for atom in _get_atoms_fn(example):
          if atom not in atoms_1:
            flag_2 = True
      if flag_2 == True: continue
      # break

      compound_divergence_in = mcd_utils.measure_example_divergence(
          examples_in_1, examples_in_2, _get_compounds_fn)
      print(compound_divergence_in)
      continue
      #self.assertEqual(compound_divergence_in, 0.8)
      # print(compound_divergence_in)
      div_sum += compound_divergence_in
      cnt += 1
      examples_out_1, examples_out_2 = mcd_utils.swap_examples(
          examples_in_1, examples_in_2, _get_compounds_fn, _get_atoms_fn, 
          print_frequencies=False,direction='max')

      # print(examples_out_1, examples_out_2)
      compound_divergence_out = mcd_utils.measure_example_divergence(
          examples_out_1, examples_out_2, _get_compounds_fn)


      r_examples_out_1, r_examples_out_2 = mcd_utils.swap_examples(
          examples_in_1, examples_in_2, _get_compounds_fn, _get_atoms_fn, 
          print_frequencies=False,direction='min')
      
      r_compound_divergence_out = mcd_utils.measure_example_divergence(
          r_examples_out_1, r_examples_out_2, _get_compounds_fn)
        
      #rounding
      compound_divergence_out = round(compound_divergence_out, 2)
      r_compound_divergence_out = round(r_compound_divergence_out, 2)

      if compound_divergence_out > max_divergence:
        max_divergence = compound_divergence_out
        e1 = examples_out_1
        e2 = examples_out_2
        maxs = {'-'.join(e1)}
        max_samples = [(e1, e2)]

      elif compound_divergence_out == max_divergence:

        e1 = examples_out_1
        e2 = examples_out_2
        maxs.add('-'.join(e1))
        if len(max_samples) < max_sample_cnt:
          if (e1, e2) not in max_samples:
            max_samples.append((e1, e2))
        compound_divergence = mcd_utils.measure_example_divergence(
          e1, e2, _get_compounds_fn)
        compound_divergence = mcd_utils.measure_example_divergence(
          e2, e1, _get_compounds_fn)
        x = 1
      
      if r_compound_divergence_out < min_divergence:
        min_divergence = r_compound_divergence_out
        e1 = r_examples_out_1
        e2 = r_examples_out_2
        mins = {'-'.join(e1)}
        min_samples = [(e1, e2)]

      elif r_compound_divergence_out == min_divergence:
        e1 = r_examples_out_1
        e2 = r_examples_out_2
        mins.add('-'.join(e1))
        if len(min_samples) < min_sample_cnt:
          if (e1, e2) not in min_samples:
            min_samples.append((e1, e2))

    # print(round(div_sum/cnt,3), max_divergence, len(maxs), min_divergence, len(mins))
    # print("my test end")
  
  '''
  def test_get_all_compounds(self):
    examples = ["jump twice", "walk twice", "jump thrice", "look and walk"]
    compounds_to_count = mcd_utils.get_all_compounds(examples,
                                                     _get_compounds_fn)

    expected_compounds_to_count = {
        "jump twice": 1,
        "walk twice": 1,
        "jump thrice": 1,
        "look and": 1,
        "and walk": 1
    }
    #self.assertDictEqual(expected_compounds_to_count, compounds_to_count)

  def test_compute_divergence(self):
    compound_counts_1 = {"a": 1, "b": 2, "c": 3}  # sum = 6
    compound_counts_2 = {"b": 4, "c": 5, "d": 6}  # sum = 15
    coef = 0.1

    divergence = mcd_utils.compute_divergence(compound_counts_1,
                                              compound_counts_2, coef)

    expected_divergence = 1.0 - (((2 / 6)**0.1 * (4 / 15)**0.9) +
                                 ((3 / 6)**0.1 * (5 / 15)**0.9))

    #self.assertAlmostEqual(expected_divergence, divergence)
  '''
  def test_max_divergence(self):
    tot = list()
    ratio = 0.5
     
    for a in ['a1', 'a2']:
      for b in ['b1', 'b2']:
        for c in ['c1', 'c2', 'c3']:
          for d in ['d1', 'd2', 'd3', 'd4', 'd5']:
            tot.append(a+' '+b+' '+c+' '+d)
    
    '''
    for a in ['a1', 'a2', 'a3']:
      for b in ['b1', 'b2']:
        for c in ['c1', 'c2']:
          tot.append(a+' '+b+' '+c)
    '''
    max_divergence = -0.1
    min_divergence = 1.1

    for i in range(30000):
      examples_in_1 = random.sample(tot, int(len(tot)*ratio))
      # examples_in_1 = random.sample(tot, 5)
      # examples_in_1 = random.sample(tot, int(len(tot)-1))
      examples_in_2 = list(set(tot) - set(examples_in_1))
      #examples_in_1, examples_in_2 = mcd_utils.balance_atoms(examples_in_1, examples_in_2, _get_atoms_fn, 1000, 1)
      
      atoms_2 = set()
      atoms_1 = set()
      for example in examples_in_1:
        atoms_1 = atoms_1.union(_get_atoms_fn(example))
      for example in examples_in_2:
        atoms_2 = atoms_2.union(_get_atoms_fn(example))
      
      flag_1 = False
      flag_2 = False
      
      for example in examples_in_1:
        for atom in _get_atoms_fn(example):
          if atom not in atoms_2:
            flag_1 = True
      # if flag_1 == True: continue

      for example in examples_in_2:
        for atom in _get_atoms_fn(example):
          if atom not in atoms_1:
            flag_2 = True
      if flag_2 == True: continue

      compound_divergence_in = mcd_utils.measure_example_divergence(
          examples_in_1, examples_in_2, _get_compounds_fn)
      
      if compound_divergence_in > max_divergence:
        max_divergence = compound_divergence_in
        e1 = examples_in_1
        e2 = examples_in_2
        maxs = {'-'.join(e1)}
      elif compound_divergence_in == max_divergence:
        e1 = examples_in_1
        e2 = examples_in_2
        maxs.add('-'.join(e1))
      if compound_divergence_in < min_divergence:
        min_divergence = compound_divergence_in
        e1_ = examples_in_1
        e2_ = examples_in_2
        mins = {'-'.join(e1_)}
      elif compound_divergence_in == min_divergence:
        e1_ = examples_in_1
        e2_ = examples_in_2
        mins.add('-'.join(e1_))

    #print(max_divergence)
    #mcd_utils.print_compound_frequencies(e1, e2, _get_compounds_fn)
    #print(min_divergence)
    #mcd_utils.print_compound_frequencies(e1_, e2_, _get_compounds_fn)
    print(max_divergence, len(maxs))
    print(min_divergence, len(mins))

  def test_swap_examples_proof(self):
    print("my test start")
    #examples_in_1 = ["a1 b1 c1", "a2 b2 c2", "a2 b1 c2", "a1 b2 c2"]
    #examples_in_2 = ["a2 b1 c1", "a2 b2 c1", "a1 b2 c1", "a1 b1 c2"]

    #examples_in_1 = ["a1 b1 c1", "a2 b2 c2", "a2 b1 c2", "a2 b1 c1", "a3 b1 c1", "a3 b2 c2"]
    #examples_in_2 = ["a1 b2 c2", "a2 b2 c1", "a1 b2 c1", "a1 b1 c2", "a3 b1 c2", "a3 b2 c1"]

    tot = list()
    for a in ['a1', 'a2', 'a3', 'a4', 'a5']:
      for b in ['b1', 'b2', 'b3', 'b4', 'b5']:
        for c in ['c1', 'c2', 'c3', 'c4', 'c5']:
          for d in ['d1', 'd2', 'd3', 'd4', 'd5']:
            for e in ['e1', 'e2', 'e3', 'e4', 'e5']:
              for f in ['f1', 'f2', 'f3', 'f4', 'f5']:
                for g in ['g1', 'g2', 'g3', 'g4', 'g5']:
    # for a in ['a1', 'a2', 'a3', 'a4']:
    #   for b in ['b1', 'b2', 'b3', 'b4']:
    #     for c in ['c1', 'c2', 'c3', 'c4']:
          # for d in ['d1', 'd2', 'd3', 'd4']:
    #         for e in ['e1', 'e2', 'e3', 'e4']:
    #           for f in ['f1', 'f2', 'f3', 'f4']:
    #             for g in ['g1', 'g2', 'g3', 'g4']:
                    tot.append(a+' '+b+' '+c+' '+d+' '+e+' '+f+' '+g)
                    # tot.append(a+' '+b+' '+c+' '+d+' '+e+' '+f)
              # tot.append(a+' '+b+' '+c)
              #tot.append(a+' '+b+' '+c+' '+d)
              #tot.append(a+' '+b)
    max_divergence = -0.1
    min_divergence = 1.1
    ratio = 0.5
    max_sample_cnt=10 
    min_sample_cnt=10
    div_sum = 0.
    times = 2
    cnt = 0
    for i in range(times):
      # if i%int(times/10) == 0: print(i)
      examples_in_1 = random.sample(tot, int(len(tot)*ratio))
      # examples_in_1 = random.sample(tot, 5)
      # examples_in_1 = random.sample(tot, int(len(tot)-1))
      examples_in_2 = list(set(tot) - set(examples_in_1))
      #examples_in_1, examples_in_2 = mcd_utils.balance_atoms(examples_in_1, examples_in_2, _get_atoms_fn, 1000, 1)
      
      atoms_2 = set()
      atoms_1 = set()
      for example in examples_in_1:
        atoms_1 = atoms_1.union(_get_atoms_fn(example))
      for example in examples_in_2:
        atoms_2 = atoms_2.union(_get_atoms_fn(example))
      
      flag_1 = False
      flag_2 = False
      
      for example in examples_in_1:
        for atom in _get_atoms_fn(example):
          if atom not in atoms_2:
            flag_1 = True
      if flag_1 == True: continue

      for example in examples_in_2:
        for atom in _get_atoms_fn(example):
          if atom not in atoms_1:
            flag_2 = True
      if flag_2 == True: continue
      # break

      compound_divergence_in = mcd_utils.measure_example_divergence(
          examples_in_1, examples_in_2, _get_compounds_fn)
      #self.assertEqual(compound_divergence_in, 0.8)
      # print(compound_divergence_in)
      div_sum += compound_divergence_in
      cnt += 1
      examples_out_1, examples_out_2 = mcd_utils.swap_examples(
          examples_in_1, examples_in_2, _get_compounds_fn, _get_atoms_fn, 
          print_frequencies=False,direction='max', max_iterations=200000)

      # print(examples_out_1, examples_out_2)
      compound_divergence_out = mcd_utils.measure_example_divergence(
          examples_out_1, examples_out_2, _get_compounds_fn)

        
      #rounding
      compound_divergence_out = round(compound_divergence_out, 3)

      if compound_divergence_out > max_divergence:
        max_divergence = compound_divergence_out
        e1 = examples_out_1
        e2 = examples_out_2
        maxs = {'-'.join(e1)}
        max_samples = [(e1, e2)]

      elif compound_divergence_out == max_divergence:

        e1 = examples_out_1
        e2 = examples_out_2
        maxs.add('-'.join(e1))
        if len(max_samples) < max_sample_cnt:
          if (e1, e2) not in max_samples:
            max_samples.append((e1, e2))
        compound_divergence = mcd_utils.measure_example_divergence(
          e1, e2, _get_compounds_fn)
        compound_divergence = mcd_utils.measure_example_divergence(
          e2, e1, _get_compounds_fn)
        x = 1
      


    print(div_sum/cnt, max_divergence, len(maxs))
    print("my test end")

if __name__ == "__main__":
  # tf.test.main()
  test = McdUtilsTest()
  # test.test_max_divergence()
  test.test_swap_examples()
  # test.test_swap_examples_proof()