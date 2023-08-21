## Compositional Testing Benchmark for Open-Domain Controllable Text Generation
### Datasets
#### 1. Amazon Reviews
2 attributes: "sent", "topic"  
"sent"$\in${"pos","neg"}  
"topic"$\in${"books", "clothing", "music", "electronics", "movies", "sports"}

#### 2. FYelp(v.1)
3 attributes: "sentiment", "gender", "cuisine"  
"sentiment"$\in${"Pos","Neg"}  
"gender"$\in${"Male","Female"}  
"cuisine"$\in${"Asian","American","Mexican","Bar","Dessert"}  
Below is an example:
```
{
    "gender": "Male",
    "sentiment": "Pos",
    "cuisine": "Bar",
    "review": "love going here for happy hour or dinner ! great patio with fans to beat the stl heat ! also ... very accomodating at this location . i like the veal milanese but with mixed greens instead of pasta ! they 'll modify the menu to suit your taste !\n"
}
```
#### 3. FYelp(v.2)
3 attributes: "sentiment", "gender", "cuisine"  
"sentiment"$\in${"Pos","Neg","Neu"}  
"gender"$\in${"Male","Female"}  
"cuisine"$\in${"Asian","American","Mexican","Bar","Dessert"}  
Below is an example:
```
{
    "gender": "Male",
    "sentiment": "Pos",
    "cuisine": "Bar",
    "review": "love going here for happy hour or dinner ! great patio with fans to beat the stl heat ! also ... very accomodating at this location . i like the veal milanese but with mixed greens instead of pasta ! they 'll modify the menu to suit your taste !\n"
}
```
#### 4. FYelp(v.3)
4 attributes: "sentiment", "gender", "cuisine", "tense"  
"sentiment"$\in${"Pos","Neg"}  
"gender"$\in${"Male","Female"}  
"cuisine"$\in${"Asian","American","Mexican","Bar","Dessert"}  
"tense"$\in${"present","past"}  
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
#### 5. FYelp(v.4)
4 attributes: "sentiment", "gender", "cuisine", "tense"  
"sentiment"$\in${"Pos","Neg","Neu"}  
"gender"$\in${"Male","Female"}  
"cuisine"$\in${"Asian","American","Mexican","Bar","Dessert"}  
"tense"$\in${"present","past"}  
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
#### 6. Yelp
3 attributes: "sentiment", "pronoun", "tense" 
"sentiment"$\in${"pos","neg"}  
"pronoun"$\in${"plural","singular"}
"tense"$\in${"present","past"}

#### 7. Mixture(IMDB, OpeNER and Sentube)
2 attributes: "sentiment", "topic_cged" 
"sentiment"$\in${"pos","neg"}  
"topic_cged"$\in${"imdb", "opener", "tablets", "auto"}

### Usage
Basically, you can refer to `test_load_dataset.py` and view the code in the `load_dataset.py`.  
1. Construction of the classifer data : training/dev/testing (70% : 15% : 15%)
2. Construction of the generator training data: HoldOut/MCD(max-avg-min)/FewShot(max-avg-min)
3. Details on constructing the MCD/Few-Shot training set for generator:  
TODO

