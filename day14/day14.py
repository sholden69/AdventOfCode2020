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
    
def apply_mask(m,opr):
    # takes the string mask and applies it to opr and then returns the number
    # convert operand to a binary string
    op_str=binary_string(opr)
    # apply mask to binary string
    ms=mask_string(m,op_str)
    res=un_binary_string(ms)
   # print('applying',m,'to',opr,'gets',res)
    return res
    
msk,inst=parse_input('day14_input.txt')

print(msk,inst)
my_mem={} #initialise a dictionary for the results
for m,i in zip (msk,inst):
    print('this mask',m,'inst list',i)
    #iterate through each instruction i i
    for i_n in i:
        #apply msk to i_n to get res
        res=apply_mask(m,i_n[1])
        my_mem[i_n[0]]=res
        print('mem',i_n[0],'=',res,'(was)',i_n[1])
# now calc totals
tot=0
for k,v in my_mem.items():
    tot+=v        
print(my_mem,'total',tot)
