import itertools, collections,copy


def range_split(inp):
    vals=inp.split('-')
    return [int(vals[0]),int(vals[1])]

class ticket_rule:
    def __init__(self):
        self.field=''
        self.range1=[0,0]
        self.range2=[0,0]
    
    def __init__(self,strFile):
        # use the string from the file input
        # departure location: 49-920 or 932-950
        self.field=strFile.split(':')[0]
        rem=strFile.split(':')[1][1:]
        i=rem.index(' or ')
        self.range1=range_split(rem[:i])
        self.range2=range_split(rem[i+4:])
        
    def display(self):
        print('field',self.field,'range1',self.range1,'range2',self.range2)
        
    def invalid_fields(self,tkt):
        #takes a ticket which is a list of integers and returns a list of invalid fields
        res=[]
        for t in tkt:
            if ((t not in range(self.range1[0],self.range1[1]+1)) & (t not in range(self.range2[0],self.range2[1]+1))):
                res.append(t)
        return res
    
    def valid_fields(self,tkt):
        #takes a ticket which is a list of integers and returns a list of valid fields
        res=[]
        for t in tkt:
            if ((t  in range(self.range1[0],self.range1[1]+1)) | (t  in range(self.range2[0],self.range2[1]+1))):
                res.append(t)
        return res
    
    def field_range_check(self,fld):
        #checks just this one fld against this rule
        return (fld  in range(self.range1[0],self.range1[1]+1)) | (fld  in range(self.range2[0],self.range2[1]+1))     
            
            
    
def find_valid_mapping(ticklist,rulelist):
    #uses permutations to try out all the different mapping possibilites. runs out of memory with 20
    nf=len(ticklist[0])
    mapping_perms=list(itertools.permutations(range(1,nf+1)))
    print(mapping_perms)
    vld_map=[]
    for mp in mapping_perms:
        err_count=0
        for tk in ticklist: #[[3, 9, 18], [15, 1, 5], [5, 14, 9]]
            for idx,fld in enumerate(tk):
                target_rule=rulelist[mp[idx]-1]
                if not target_rule.field_range_check(fld):
                    err_count+=1
                    break
            if err_count>0:
                break
        if err_count==0:
            vld_map=mp
            break;
    return vld_map

def prod(curr, *others):
    if not others:
        for x in curr:
            yield {x} # (x,) for tuples
    else:
        for o in prod(*others):
            for c in curr:
                if c not in o:
                    yield {c, *o} # (c, *o) for tuples

def gen_valids (inplist):
    if len(inplist)==0:
        #print('bottomed out',inplist)
        return inplist
    hd=inplist[0]
    tl=inplist[1:]
   # print('call to gen_valids','inp',inplist,'head/tail',hd,'/',tl)
    res=[]
    ret=gen_valids(tl)
   # print('inplist len',len(inplist),'got back',ret,'for',tl,'retlist len',len(ret))
    for el in hd:
        print('trying',el,'from',hd,'vs',tl,'res',res)   
        if ret==[]:
            tmp=[el]
            res.append(tmp)
        else:
            for r in ret:
                #print('head',hd,'tail',tl,'looking for',el,'in',r,'out of',ret)
                if not el in r:
                    tmp=copy.deepcopy(r)
                    tmp.append(el)
                    res.append(tmp)
                   # print('bingo',res)
 #   print('finished hd',hd,'result=',res)
    return res



def find_valid_mapping3 (ticklist,rulelist):
 #uses permutations to try out all the different mapping possibilites. runs out of memory with 20
    nf=len(ticklist[0])
    # build a list of lists showing for each mapping which would have no errors. Can combine to pick best from there.
    res_list=[]
    for source in range(1,nf+1):
        this_row=[]
        for dest in range(1,nf+1):
            #see how many errors you get when source field maps to rule dest, trying each ticket in turn
            err_count=0
            for tk in ticklist:
                target_rule=rulelist[dest-1]
                if not target_rule.field_range_check(tk[source-1]):
                    err_count+=1
                    break
            if err_count==0:
                # this mapping doesnt fail
                this_row.append(dest)
        res_list.append(this_row)
    res=prod(*res_list)
    for r in res:
        vld_map=list(r)
    return vld_map


def find_valid_mapping2(ticklist,rulelist):
    #uses permutations to try out all the different mapping possibilites. runs out of memory with 20
    nf=len(ticklist[0])
    # build a list of lists showing for each mapping which would have no errors. Can combine to pick best from there.
    res_list=[]
    for source in range(1,nf+1):
        this_row=[]
        for dest in range(1,nf+1):
            #see how many errors you get when source field maps to rule dest, trying each ticket in turn
            err_count=0
            for tk in ticklist:
                target_rule=rulelist[dest-1]
                if not target_rule.field_range_check(tk[source-1]):
                    err_count+=1
                    break
            if err_count==0:
                # this mapping doesnt fail
                this_row.append(dest)
        res_list.append(this_row)
    print(res_list)

    # build up the list of maps iteratively to avoid memory errors
    i=0
    interim=[res_list[0]]
    while i<(nf-1):
        interim.append(res_list[i+1])
        thismp=list(itertools.product(*interim))
        for idx,m in enumerate(thismp):
            occurrences = collections.Counter(m)
            valid=True
            for occ,val in occurrences.items():
                valid=(val==1)
                if not valid: break  #stop counting
            if not valid: thismp.remove(m)
        interim=thismp
     #   for j in thismp:
     #       interim.append(list(j))
        # flatten list of lists 
        i+=1
    print(interim)
    return(interim)
   # print(res_list,output)
                    
def find_valid_mapping4(ticklist,rulelist):
    #uses permutations to try out all the different mapping possibilites. runs out of memory with 20
    nf=len(ticklist[0])
    # build a list of lists showing for each mapping which would have no errors. Can combine to pick best from there.
    res_list=[]
    for source in range(1,nf+1):
        this_row=[]
        for dest in range(1,nf+1):
            #see how many errors you get when source field maps to rule dest, trying each ticket in turn
            err_count=0
            for tk in ticklist:
                target_rule=rulelist[dest-1]
                if not target_rule.field_range_check(tk[source-1]):
                    err_count+=1
                    break
            if err_count==0:
                # this mapping doesnt fail
                this_row.append(dest)
        res_list.append(this_row)
    print(res_list)
    res=gen_valids(res_list)
    print('map',res)
    return res
   
   # print(res_list,output) 

#***************************** Main prog ***************************************

with open('day16_input_test2.txt') as f:
    lines = [x for x in f.read().splitlines()]

global gl_res_list
# read the rules, my ticket, other tickets
i=0
line=lines[0]
rules=[]
while (line!='your ticket:'):
    #print(line)
    if line!='':
        rules.append(ticket_rule(line))
        #parse the rule into tuple: String, range1 [a,b], range2 [a,b]
    i+=1
    line=lines[i]
    
# read my ticket
m=lines[i+1].split(',')
myticket = list(map(int, m))

# pull out the nearby tickets
i+=4
nearbys=[]
while (i<len(lines)) :
    n=lines[i].split(',')
    nearbys.append(list(map(int,n)))
    i+=1

print('** RULES **')
for tr in rules:
    tr.display()

tot=0
vld_ticks=[]
for tk in nearbys:
    valids=[]
    for tr in rules:
        vt=tr.valid_fields(tk)
        #print('validating',tk,'against')
        #tr.display()
        #print('gives',vt)
        for v in vt: 
            valids.append(v)
    vset=set(valids)
    # now find all the invalid ticket numbers not in vset
    vld=True
    for fld in tk: 
        if fld not in vset: 
            tot+=fld
            vld=False
    if vld:
        vld_ticks.append(tk)
print('Part 1 solution',tot)
    
#now we have a set of valid tickets in vld_ticks
print('Valid tickets are',vld_ticks)
nfields=len(nearbys[0])

# need to come up with a mapping of ticket_field -> rule-field which means every ticket is in range
# that can be a dict{ticket_field}->rule-field
vld_map=find_valid_mapping4(vld_ticks,rules)
vld_map=vld_map[0]
print(vld_map)

#use vld_map to parse my ticket
tot=0
for idx,fld in enumerate(myticket):
    target_rule=rules[vld_map[idx]-1]
    print (target_rule.field,'my ticket field value',fld)

