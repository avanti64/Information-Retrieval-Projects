'''
Created on Oct 11, 2014

@author: Avanti
'''
import sys
from collections import defaultdict
import math
import operator

#Function to calculate perplexity
def calculate_perplexity(page_rank):
    perplexity = 0
    entropy = 0
    for value in page_rank.values():
        entropy+= (-value*(math.log(value,2)))
    perplexity=math.pow(2,entropy)
    return perplexity

#-----------------------------------------------------------------------------------------------#
#Initialization of the dictionaries and sets 

page_rank = {}
in_links_count={}
newpageRank = {}
sorted_pagerank = {} 
sink_nodes = set()

#-----------------------------------------------------------------------------------------------#
#print("Starting program")
distinct_page = set()
in_links = defaultdict(set)
out_links = defaultdict(set)
f = open(sys.argv[1])
N = 0
#Get the data from the file and process it 
for line in f:
        N = N+1
        lineList =  line.strip().split(" ")
        destination = lineList[0]
        sourceList =  lineList[1:]
        for p in sourceList:
            in_links[destination].add(p)
            out_links[p].add(destination)
        distinct_page.add(destination)
        in_links_count.update({destination:len(in_links[lineList[0]])})
f.close()

#Initialize page rank as per pseudo code 1/N    
for p in distinct_page:
    page_rank[p] = 1/float(N)

#Find sink nodes
for j in distinct_page:
        if len(out_links[j]) == 0:
            sink_nodes.add(j)
        
i=1
current_perplexity = calculate_perplexity(page_rank)
prev_perplexity = 0
n=0
graph_size = len(distinct_page)
converged = 5
#-----------------------------------------------------------------------------------------------#
#Pseudocode implementation
while i!=5:
    if(current_perplexity-prev_perplexity) < 1:
        i+=1
    else:
        i=1
    
    sinkPR = 0
    n=n+1
    print (current_perplexity)
    for page_sink in sink_nodes:
        sinkPR += page_rank[page_sink]
        
    for page in distinct_page:
        newpageRank[page]=(1.0-0.85)/graph_size
        newpageRank[page]= newpageRank[page]+ ((0.85*sinkPR)/graph_size)
        for q in in_links[page]:
            newpageRank[page]+=(0.85*page_rank[q]/len(out_links[q]))
    for page in distinct_page:
        page_rank[page]=newpageRank[page]
    
    prev_perplexity=current_perplexity
    current_perplexity = calculate_perplexity(page_rank)
#Sorting 
sorted_pagerank = (sorted(page_rank.items(),key=operator.itemgetter(1), reverse=True))
f = open("page_rank_sorted.txt", 'w')
f2 = open("inlink_sorted.txt", 'w')
for i in range(0,50):
    f.write("%s\n" % str(sorted_pagerank[i]))
f.close()
in_link_count = (sorted(in_links_count.items(),key=operator.itemgetter(1), reverse=True))
for i in range(0,50):
    f2.write("%s\n" % str(in_link_count[i]))
f2.close()