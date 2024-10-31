## Implementation of 3-dimensional Testing Protocols (HoldOut, ACD and FewShot) for CompMCTG
This repo contains the implementation of of 3-dimensional Testing Protocols (HoldOut, ACD and FewShot) for CompMCTG (the main repo can be found here: https://github.com/tqzhong/CG4MCTG.)
### Datasets
#### 1. Amazon Reviews
2 attributes: "sent", "topic"  
1. "sent"$\in${"pos","neg"}  
2. "topic"$\in${"books", "clothing", "music", "electronics", "movies", "sports"}

#### 2. FYelp(v.3)
4 attributes: "sentiment", "gender", "cuisine", "tense"  
1. "sentiment"$\in${"Pos","Neg"}  
2. "gender"$\in${"Male","Female"}  
3. "cuisine"$\in${"Asian","American","Mexican","Bar","Dessert"}  
4. "tense"$\in${"present","past"}  
Below is an example:
```
{
    "gender": "Male",
    "sentiment": "Pos",
    "cuisine": "Bar",
    "tense": "Present",
    "review": "love going here for happy hour or dinner ! great patio with fans to beat the stl heat ! also ... very accomodating at this location . i like the veal milanese but with mixed greens instead of pasta ! they 'll modify the menu to suit your taste !\n"
}
```
#### 3. Yelp
3 attributes: "sentiment", "pronoun", "tense"  
1. "sentiment"$\in${"pos","neg"}  
2. "pronoun"$\in${"plural","singular"}  
3. "tense"$\in${"present","past"}

#### 4. Mixture(IMDB, OpeNER and Sentube)
2 attributes: "sentiment", "topic_cged"  
1. "sentiment"$\in${"pos","neg"}  
2. "topic_cged"$\in${"imdb", "opener", "tablets", "auto"}

### Usage: For Constructing Training / Testing Sets (w. HoldOut, ACD and Few-Shot Protocols)
Basically, you can refer to the inferences in `test_load_dataset.py` and view the code in the `load_dataset.py`.  
1. Construction of the classifer data : training/dev/testing (70% : 15% : 15%)
2. Construction of the generator training data: HoldOut/MCD(max-avg-min)/FewShot(max-avg-min)

### Acknowledgement:
The implementation is on the basis of Google Research's implementation of TMCD (https://github.com/google-research/language/tree/master/language/compgen/nqg, "Compositional Generalization and Natural Language Variation: Can a Semantic Parsing Approach Handle Both?", ACL'2021).
