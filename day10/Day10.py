import itertools
import time

def get_adapter_list (fl,toptail):
    with open(fl) as f:
        nbrs = [int(x) for x in f.read().split()]
    nbrs=sorted(nbrs)
    my_device=int(nbrs[-1])+3
    if toptail:  #put the outlet and mydevice on it
        nbrs.append(my_device)
        nbrs.append(0)
    return sorted(nbrs)

def is_valid_list (lst):
    #check that no gap is > 3
    for i in range(len(lst)-1):
        if lst[i+1]-lst[i]>3:
            return False
    return True

def count_lists (lst):
    cnt=0
    if is_valid_lst(lst):
        cnt=cnt+1


def slow_one():
    ttl=0
    ls=get_adapter_list('day10_input.txt',False)
    my_device=ls[-1]+3
    ln=len(ls)
    print("there are",ln,"items in the list")
    #work out a min length my_device/3
    for L in range(int(my_device/3), ln+1):
        print("finding all combos of length", L)
        for subset in itertools.combinations(ls, L):
            outlet=tuple('0')
            final_combo=(0,) + subset + (my_device,)
            if ((my_device-final_combo[-2]<=3) & (final_combo[0]<=3)): #test at the start and end
               # print(final_combo)
                if is_valid_list(final_combo):
                   # print('valid:',final_combo)
                    ttl+=1
    print(ttl,"valid combos")

def valid_list(hd,lst):
    if (len(lst)<=1) :
        #print(hd,lst,"**bingo**")
        return 1
    i=0
    success=0
    done=False
    #print ("going into while loop",lst,hd)
    # look down the list for every element that could be a valid next element for hd, and try to find a valid list wth them
    while not done :
        if ((lst[i]-hd)<=3) : #these two elements are good
            #print(hd,lst[i],"are good.")
            #print("now try",lst[i],lst[i+1:])
            success+=valid_list(lst[i],lst[i+1:])
        else: #no more elements on this line to look at
            #print("break out",hd,lst[i])
            done=True
            break
        i+=1
        done = ((i+1)==len(lst))
    #print('success is up to',success)
    return success


def faster_one():
    #55 - 10s - 4917248
    #57 - 18s - 9834496  . last element 92
    #58 - 29s  - 19668992. last element 95
    #59 - 41- 19668992
    #60 - 52s - 19668992
    #61 - 64s - 19668992
    #62 - 86s - 39337984
    #65 - 174 - 78675968

    t0 = time.time()
    ls=get_adapter_list('day10_input.txt',True)
    ls=ls[:65]
    print(len(ls))
    print("full list",ls)
    print("result:",valid_list(ls[0],ls[1:]))
    t1 = time.time()
    print("in time",t1-t0)
    

def generate_edges(graph):
    edges = []
    for node in graph:
        for neighbour in graph[node]:
            edges.append((node, neighbour))

    return edges


 
    
graph={}
has_result=[]
results=[]

def count_routes(start,end):
    #count all the routes that end in end, starting at start. use the cache to avoid repeat traversals
  #  print('count_routes',start,end)
    if (start==end):
        return 1
    else:
        success=0
       # print('going through nodes for start=',start)
        for i in graph[start]:
            #print('checking',i,'..',end)
            if (has_result[i]):
                res=results[i]
            else:
                res=count_routes(i,end)
                has_result[i]=True
                results[i]=res
            success+=res
        return success
    
def build_day10_graph (fl):
    ls=get_adapter_list(fl,True)  
    #ls=ls[:65]
    print(ls)
    list_len=len(ls)
    for i in range((list_len)-1):
        good_nodes=[]
        j=i+1  #start from the item after i
        done=False
    #    print('checking out item',i)
        while not done:
            if (ls[j]-ls[i])<=3:
                good_nodes.append(ls[j])
            else:
                break
            j+=1
            done=(j>=list_len)
        graph[ls[i]]=good_nodes
    
    # pop a node to nowhere on the end
    last_key=ls[-1:][0]
    graph[last_key]=[]  #add a null node for the end
    return(last_key,ls)

t0 = time.time()
lk,ls=build_day10_graph('day10_input.txt')
print(graph)

#initiate the cache
has_result=[False]*(lk+1)
results=[0]*(lk+1)

# now count, but cache will be used every time a route that has been calculated  is requested
print(count_routes(0,lk))
t1 = time.time()
print("in time",t1-t0)


