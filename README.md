## Compositional Testing Benchmark for Open-Domain Controllable Text Generation
### Datasets
#### 1. Amazon Reviews
2 attributes: "sent", "topic" 
"sentiment"$\in${"pos","neg"}  
"topic"$\in${"books", "clothing", "music", "electronics", "movies", "sports"}

#### 2. FYelp(v.1)
3 attributes: "sentiment", "gender", "cuisine"  
"sentiment"$\in${"Pos","Neg"}  
"gender"$\in${"Male","Female"}  
"cuisine"$\in${"Asia","American","Mexican","Bar","Dessert"}  
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
"cuisine"$\in${"Asia","American","Mexican","Bar","Dessert"}  
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
"cuisine"$\in${"Asia","American","Mexican","Bar","Dessert"}  
"tense"$\in${"Present","Past"}  
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
"cuisine"$\in${"Asia","American","Mexican","Bar","Dessert"}  
"tense"$\in${"Present","Past"}  
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
3 attributes: "sentiment", "person", "tense" 
"sentiment"$\in${"Pos","Neg"}  
"person"$\in${"Plural","Singular"}
"tense"$\in${"Present","Past"}

#### 7. IMDB
3 attributes: "sentiment", "person", "tense" 
"sentiment"$\in${"Pos","Neg"}  
"person"$\in${"Plural","Singular"}
"tense"$\in${"Present","Past"}

#### 8. Mixture(IMDB, OpeNER and Sentube)
2 attributes: "sentiment", "topic_cged" 
"sentiment"$\in${"pos","neg"}  
"topic_cged"$\in${"movie", "hotel", "tablet", "automobie"}