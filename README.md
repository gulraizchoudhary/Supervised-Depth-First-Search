# Supervised Depth First Search Approach
This approach is developed to study frequent sub-sequences in temoral disease occurrence network. The network is constructed using ICD-10 disease codes used to mark the patient diseases. These diagnosis are (ICD-10 disease codes) temporaly assigned to a patient during their visit to health center. The sequence contains temporal information that patient were assigned ICD-10 code at different times as the disease has progressed. The comorbid patients often contract other chronic diseases. In other words severity increase with passage of time and it can be delayed with better understanding and improving healthy life style. For example retrieving the frequent sub-sequences to study the common disease complications and progressions in patient cohorts.

## Example 1: 

```python

#sample json keys are labels and list contains sequences (A sequence can a be a set of temporal ICD-10 codes)
    data = {'1': {'gender':'M' ,'age_group':'20-30', 'sequence': ['B', 'D', 'E']},
             '2':{'gender':'M','age_group':'30-40', 'sequence': ['B', 'D', 'E']},
             '3': {'gender':'F','age_group':'20-30','sequence':['A', 'F']},
             '4': {'gender':'F','age_group':'20-30', 'sequence':['B','A', 'F']},
             '5': {'gender':'M', 'age_group':'20-30', 'sequence':['B', 'D', 'C']},
             '6': {'gender':'M', 'age_group':'20-30', 'sequence':['B', 'D', 'C']},
             '7': {'gender':'M', 'age_group':'20-30', 'sequence':['B', 'D', 'C']},
             '8': {'gender':'M', 'age_group':'20-30', 'sequence':['B', 'D', 'C']},
             '9': {'gender':'M', 'age_group':'20-30', 'sequence':['B', 'D', 'C']},
             '10': {'gender':'F', 'age_group':'20-30', 'sequence': ['A', 'F','G']}}
    #INPU: relative minsupport for each gender and each group
    graph = Graph(0.01, data)
    
    print(graph.dfs('B', '30-40', 'M'))
	
```
## Output
```bash
[(['B', 'D'], 1), (['B', 'D', 'E'], 1)]

```



## Acknowledgements
Please cite our paper:<br>
G. I. Choudhary and P. Fränti, Predicting onset of disease progression using temporal disease occurrence network (in progress)
School of Computing, University of Eastern Finland


## License
[MIT](https://choosealicense.com/licenses/mit/)
