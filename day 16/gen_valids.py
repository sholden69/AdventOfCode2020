import copy

def gen_valids (inplist):
    if len(inplist)<=1:
        #print('bottomed out',inplist)
        return inplist
    hd=copy.deepcopy(inplist[0])
    tl=copy.deepcopy(inplist[1:])
    #print('call to gen_valids','inp',inplist,'head/tail',hd,'/',tl)
    res=[]
    ret=gen_valids(tl)
    #print('inplist len',len(inplist),'got back',ret,'for',tl,'retlist len',len(ret))
    for el in hd:
        #print('trying',el,'from',hd,'vs',tl,'res',res)
        if len(ret)>0:
            for r in ret:
                #print('head',hd,'tail',tl,'looking for',el,'in',r,'out of',ret)
                if not el in r:
                    tmp=copy.deepcopy(r)
                    tmp.append(el)
                    res.append(tmp)
                    #print('bingo',res)
 #   print('finished hd',hd,'result=',res)
    return res


print(gen_valids([[2,1],[1,2,3],[2]]))
