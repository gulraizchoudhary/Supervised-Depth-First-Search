# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 13:36:33 2022

@author: gulrch
"""

import networkx as nx
import copy as cpy

class Graph:
    def __init__(self, supp, data):
        self.supp = supp
        self.G = nx.DiGraph()
        self.statistics ={}
        self.diagraph(data)


    def diagraph(self, data):
        
        #iterate through the graph
        for lst, key in enumerate(data.keys()):
             
               gender = data[key]['gender']
               age_group = data[key]['age_group']
               if gender not in self.statistics:
                   self.statistics[gender]={}
                
               if age_group not in self.statistics[gender]:
                   self.statistics[gender][age_group]=1
               else:  
                   self.statistics[gender][age_group]+=1    
               
                
               start = 'STR'
               term = 'END'
               
               #Add nodes if they don't exist
               if not start in self.G.nodes:
                   self.G.add_node(start)
               if not term in self.G.nodes:
                   self.G.add_node(term)
                    
               
               flag = True
               prev = ""
               for item in data[key]['sequence']:
                  
                   #maintain frequencies of occurrence of a node in data
                   if item not in self.G.nodes():
                       self.G.add_node(item)
                       self.G.nodes[item][gender]={}
                       self.G.nodes[item][gender][age_group]={}
                       self.G.nodes[item][gender][age_group]['weight']=1               
                   else:
                       if gender not in self.G.nodes[item]:
                           self.G.nodes[item][gender]={}
                            
                       if age_group not in self.G.nodes[item][gender]:
                            self.G.nodes[item][gender][age_group]={}
                            self.G.nodes[item][gender][age_group]['weight']=1  
                       else:
                            self.G.nodes[item][gender][age_group]['weight']+=1
                   if flag:
                       flag = False
                       prev =age_group
                       
                   if not self.G.has_edge(prev, item):  
                       self.G.add_edge(prev, item)
                       self.G.edges[prev, item]['weight'] ={}
                       self.G.edges[prev, item]['weight'][gender] ={}
                       self.G.edges[prev, item]['weight'][gender][age_group] =[key]
                   else:
                       if gender not in self.G.edges[prev, item]['weight']:
                           self.G.edges[prev, item]['weight'][gender] ={}
                            
                            
                       if age_group not in self.G.edges[prev, item]['weight'][gender]:
                           self.G.edges[prev, item]['weight'][gender][age_group] =[key]
                       else:    
                           self.G.edges[prev, item]['weight'][gender][age_group].append(key)
                        
                   prev = item
                   
                #Termination node
               if not self.G.has_edge(item, term):  
                   self.G.add_edge(item, term)
                   self.G.edges[item, term]['weight'] ={}
                   self.G.edges[item, term]['weight'][gender] ={}
                   self.G.edges[item, term]['weight'][gender][age_group] =[key]
               else:
                   if gender not in self.G.edges[item, term]['weight']:
                        self.G.edges[item, term]['weight'][gender] ={}
                   if age_group not in self.G.edges[item, term]['weight'][gender]:
                        self.G.edges[item, term]['weight'][gender][age_group] =[key]
                   else:
                        self.G.edges[item, term]['weight'][gender][age_group].append(key)



    def dfs(self, start,age_group, gender):
        stack = [(start, [start],[])]
        visited = set()
        vPath = []
        
        while stack:
            (vertex, path, intersection) = stack.pop()
            
            if vertex not in visited:
               
                visited.add(vertex)
                
                for neighbor in set(self.G.successors(vertex))-set(path):
                    
                    if neighbor !='END':
                       
                        support = self.getIntersection(gender, age_group, vertex, neighbor, cpy.deepcopy(intersection))
                        
                        #Stop exploring the depth if minsupport < then the given threshold
                        if len(support)>(self.supp*self.statistics[gender][age_group]) :
                            stack.append((neighbor, path + [neighbor], cpy.deepcopy(support)))
                            vPath.append((path+[neighbor],len(support)))
                       
        return vPath

    def getIntersection(self, gender, age_group, vertex, neighbor, intersection):
        
        if gender in self.G[vertex][neighbor]['weight']:
            if age_group in  self.G[vertex][neighbor]['weight'][gender]:    
                if len(intersection)<1:
                     return set(self.G[vertex][neighbor]['weight'][gender][age_group])
                else:
                     return (set(self.G[vertex][neighbor]['weight'][gender][age_group]) & intersection)
        return set()


if __name__ == '__main__':
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
    