# ADM_group_9

This is the repository for Homework 4 of Algorithmic Methods for Data Mining - Group 9




#### From the root folder run:



```
python3 module.py
```



It is possible to choose between:


* "reduced" or "full" database; 



The program will calculate our main graph in which each node represents an author and the edges that connect them are weighted using weights=(1-Jaccard similarity). After this operation you can select the excercise to be performed choosing between the following options:


* 2a, 2b, 3a or 3b.


Each choise is related with the two exercises (part one and part two for both of them). for each one, according with the task of the exercise, you have different arguments explained in detail below. Let's go on details about each exercise.





## Exercise 2) - statistics and visualizations.



### 2a)


Since the task is to have the subgraph induced by the set of authors who published at least once in a given conference, as first output is given a list of the conference ID from which you can choose the one you prefer. 
After putting as input the ID conference, you'll receive as first output the plot of the subgraph; after closing this first figure, the program will show the histograms related to the centralities measures in the following order: degree, closeness and betweeness centralities.




### 2b)


Given an author ID as input we'll give as a result the subgraph of the nodes which have at most distance equal to a certain level, that we'll call "d". In order to provide our result, at first, you have to choose the author ID and secondly the maximum hop distance (equal to "d") that you want to check.  We used the ego_graph function belonging to the networkx library to calculate this subgraph. 




## Exercise 3) - some generalized version of the Erdos number.



### 3a)


In this one we should calculate the shortest path that connects an author chosen in input with Aris (whose ID is equal to 256176). As said, you choose an author ID and the program will give you the weight of the shortest path between it and Aris. 




### 3b)


In this last exercise you have to give as input a list of authors ID, separated by space and the program will give you a dictionary as a result containing the "GroupNumber" between all the nodes and the ID's of the input authors. If a node has no connections with noone nodes in the list it will have 'NaN' as a result, in the other case you'll have a touple containing the minimum between shortest paths (for every node in our input)
