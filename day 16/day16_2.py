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
        
       
    def valid_fields(self,tkt):
        #takes a ticket which is a list of integers and returns a list of valid fields
        res=[]
        for t in tkt:
            if ((t  in range(self.range1[0],self.range1[1]+1)) | (t  in range(self.range2[0],self.range2[1]+1))):
                res.append(t)
        #print(tkt,res)
        return res

    def valid_fields2(self,tkt):
        #takes a ticket which is a list of integers and returns a list of *valid ids*
        res=[]
        for idx,t in enumerate(tkt):
            if ((t  in range(self.range1[0],self.range1[1]+1)) | (t  in range(self.range2[0],self.range2[1]+1))):
                res.append(idx)
        #print(tkt,res)
        return res
    
    def field_range_check(self,fld):
        #checks just this one fld against this rule
        res= (fld  in range(self.range1[0],self.range1[1]+1)) | (fld  in range(self.range2[0],self.range2[1]+1))  
        #if (abs(fld-self.range1[0]) <3) |(abs(fld-self.range1[1]) <3) |(abs(fld-self.range2[0]) <3) |(abs(fld-self.range1[1]) <3)  :
         #   print(self.field,'checking',fld,'vs r1:',self.range1[0],self.range1[1],'r2:',self.range2[0],self.range2[1],'result:',res)
           
        return res 

       
class Puzzle:
    def __init__(self):
        self.nfields=0
        self.rules=[]
        self.myticket=[]
        self.nearbys=[]
        self.vld_ticks=[]
        self.tot_valid=0

    def __init__(self,fl):
        with open(fl) as f:
            lines = [x for x in f.read().splitlines()]

        # read the =rules, my ticket, other tickets
        i=0
        line=lines[0]
        self.rules=[]
        while (line!='your ticket:'):
            #print(line)
            if line!='':
                self.rules.append(ticket_rule(line))
                #parse the rule into tuple: String, range1 [a,b], range2 [a,b]
            i+=1
            line=lines[i]
        self.nfields=len(self.rules)
            
        # read my ticket
        m=lines[i+1].split(',')
        self.myticket = list(map(int, m))

        # pull out the nearby tickets
        i+=4
        self.nearbys=[]
        while (i<len(lines)) :
            n=lines[i].split(',')
            self.nearbys.append(list(map(int,n)))
            i+=1   

    
 
    def build_valid_tickets2(self):
            tot=0
            self.vld_ticks=[]
            for tk in self.nearbys:
                valids=[]
                for tr in self.rules:
                    vt=tr.valid_fields2(tk) #this returns a list of valid fi field ids
                    #print('validating',tk,'against')
                    #tr.display()
                    #print('gives',vt)
                    for v in vt: 
                        valids.append(v)
                vset=set(valids)
                # now find all the invalid ticket numbers not in vse
                vld=True
                for idx,fld in enumerate(tk): 
                    if idx not in vset: 
                        tot+=fld
                        vld=False
                if vld:
                    self.vld_ticks.append(tk)
            self.tot_invalid=tot
            #need to add myticket in as a valid ticket 
            self.vld_ticks.append(self.myticket)

    def gen_valids (self,listidx):
        if (listidx==(self.nfields-1)):
            tmp=[]
            for r in self.perms_list[self.nfields-1]:
                tmp.append([r])
            return tmp
        hd=self.perms_list[listidx]
        tl=self.perms_list[listidx+1:]
     #print('call to gen_valids','inp',inplist,'head/tail',hd,'/',tl)
        res=[]
        ret=self.gen_valids(listidx+1)
    # print('inplist len',len(inplist),'got back',ret,'for',tl,'retlist len',len(ret))
        for el in hd:
            #print('trying',el,'from',hd,'vs',tl,'res',res)   
            if ret==[]:
                tmp=[el]
                res.append(tmp)
            else:
                for r in ret:
                    #print('head',hd,'tail',tl,'looking for',el,'in',r,'out of',ret)
                    if not el in r:
                        tmp=copy.deepcopy(r)
                        tmp.insert(0,el)
                        res.insert(0,tmp)
                    # print('bingo',res)
    #   print('finished hd',hd,'result=',res)
        return res

    def apply_onseys(self):
        #filters perms_list down by sequentially looking for items with only 1 entry
        solns=set()
        for i in range (self.nfields):
            #find the item with a single row
           # print('it',i,self.perms_list,'len',len(self.perms_list))
            el_idx=-1
            for j in range (self.nfields):
                test=self.perms_list[j]
                zeroth=self.perms_list[j][0]
                #print(test,len(test))
                if (len(test)==1) & (zeroth not in solns):
                    el_idx=j
                    el_val=zeroth
                    break
           # print('solo item index:',el_idx,'value:',el_val)
            # remove el_val from all other lists
            for j in range (self.nfields):
                if j!=el_idx:
                    if el_val in self.perms_list[j]:
                            self.perms_list[j].remove(el_val)
            #print('found',el_val)
            solns.add(el_val)
        print('post onesy',self.perms_list)
        
    
    def build_perms(self):
        # build a list of lists showing for each mapping which would have no errors. Can combine to pick best from there.
        self.perms_list=[]
        for dest in range(0,self.nfields):  #this is the rule we're going to check
            this_row=[] #collect all the rul
            for chk_fld in range(0,self.nfields): #this is the field we are checking
                #see how many errors you get when source field maps to rule dest, trying each ticket in turn
                err_count=0  #count up the errors across all tickets
                for tk in self.vld_ticks:   
                    if not self.rules[dest].field_range_check(tk[chk_fld]): #check this one field against this rule
                        err_count+=1 #no point carrying on if we found an  error on any ticket
                        break
                if err_count==0:
                    # this mapping doesnt fail
                    this_row.append(chk_fld)  #this filed is this rule
            self.perms_list.append(this_row)
            #print('perms list:',self.perms_list)

    def find_valid_mapping(self):
    #uses permutations to try out all the different mapping possibilites. runs out of memory with 20   
        self.apply_onseys()
        self.map_soln=self.perms_list

        # with this version of the problem, the recursive search isnt needed
        # if you do run this you get a single list back so lose the sub-script in the final read out
        #self.map_soln=self.gen_valids(0)[0]

    def display_perms(self):
        print('** RULES + PERMS **')
        for idx,tr in enumerate(self.rules):
            tr.display()
            print(self.perms_list[idx])

 
#***************************** Main prog ***************************************

pz=Puzzle('day16_input.txt')
pz.build_valid_tickets2()
print('Part 1 solution',pz.tot_invalid)


#now we have a set of valid tickets in vld_ticks
#print(len(pz.vld_ticks),'Valid tickets are',pz.vld_ticks)

# need to come up with a mapping of ticket_field -> rule-field which means every ticket is in range
# that can be a dict{ticket_field}->rule-field
pz.build_perms()
pz.display_perms()
pz.find_valid_mapping()

#use vld_map to parse my ticket
tot=1
print("my tick",pz.myticket)
print("solution",pz.map_soln)
for rle in range(pz.nfields): #got rule by rule
    fldmap=pz.map_soln[rle][0]  #if you use gen_valids drop the [0] subscript here
    curr_rule=pz.rules[rle]
    curr_val=pz.myticket[fldmap]
    print('col',curr_rule.field,'maps to field #',fldmap,'value',curr_val)
    if curr_rule.field[:6]=="depart":
        tot=tot*curr_val
       
print("part 2 soln",tot)

