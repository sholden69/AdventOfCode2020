# initialise list of mask and list of list of instrs
def parse_input (fl):
    masks=[]
    instrs=[]
    file = open(fl, 'r') 
    lines = file.read().splitlines()
  #  print(len(lines),lines)
    i=0
    while (i<len(lines)):
        #first line is a mask
        masks.append(lines[i][7:])
        i+=1
        this_instr=[]
        while (i<len(lines)) :
            if (lines[i][0:3]=="mem"):
                mem_loc=int(lines[i][lines[i].find('[')+1:lines[i].find(']')])
                operand=int(lines[i][lines[i].find(']')+3:])
                this_instr.append([mem_loc,operand])
                # this_instr.append(int(lines[i][lines[i].find('[')+1:lines[i].find(']')]))
            else:
                break
            i+=1
        instrs.append(this_instr)
  #      print(instrs)
    return masks, instrs

def binary_string(inp):
    # takes an int and returns a 36 char binary str
    res=''
    i=35
    while (i>=0):
        if ((inp & (2**i))!=0):
            res+='1'
        else:
            res+='0'
        i-=1    
    return res

def un_binary_string(inp):
    res=0
    for i in range(36):
        dig=35-i
        if inp[i]=="1":
            res+=2**dig
    return res


def mask_string(msk,operand):
    
    # takes two 36 char strs as inputs and applies msk to operand
    mymask=msk
    res=''
    for i in range(len(mymask)):
        if mymask[i]!='X':
            res+=mymask[i]
        else:
            res+=operand[i]
    return res

def mask_string2(msk,operand):
    # part 2 mask function.
    mymask=msk
    res=''
    for i in range(len(mymask)):
        if (mymask[i]=="1" )|( mymask[i]=='X'):
            res+=mymask[i]
        else:
            res+=operand[i]
    return res
    
def apply_mask(m,opr):
    # takes the string mask and applies it to opr and then returns the number
    # convert operand to a binary string
    op_str=binary_string(opr)
    # apply mask to binary string
    ms=mask_string(m,op_str)
    res=un_binary_string(ms)
   # print('applying',m,'to',opr,'gets',res)
    return res

def expand_mem(mm):
    # return a list of 36 bit integers base on replacing all the Xs
    xlocs=[]
    for i in range(len(mm)):
        if mm[i]=="X":
            xlocs.append(i)
    nx=len(xlocs)
    max_x=2**(nx)
    perms=[]
    for i in range(max_x):
        res=[]
        for j in range(nx):
            if (i & (2**j))==(2**j):
                res+="1"
            else:
                res+="0"
        perm=''
        for k in range(len(mm)):
            if k in xlocs:
                idx=xlocs.index(k)
                perm=perm+res[idx]
            else:
                perm+=mm[k]
        perms.append(un_binary_string(perm))
    return perms


    
msk,inst=parse_input('day14_input.txt')
print(msk,inst)
my_mem={} #initialise a dictionary for the results
for m,i in zip (msk,inst):
    print('this mask',m,'inst list',i)
    #iterate through each instruction i i
    for i_n in i:
        #apply m to i_n to get res
        mem_mask=mask_string2(m,binary_string(i_n[0]))
        mem_locs=expand_mem(mem_mask)
        for mem in mem_locs:
            my_mem[mem]=i_n[1]
# now calc totals
tot=0
for k,v in my_mem.items():
    tot+=v        
print(my_mem,'total',tot)
