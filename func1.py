import csv
from itertools import combinations_with_replacement
import copy
from pkgutil import iter_modules
from re import I, X
from sre_parse import FLAGS
from certifi import contents
import pandas as pd
from sklearn.datasets import fetch_20newsgroups_vectorized
#from pkg_resources import _NestedStr
from sqlalchemy import false

def cal_length(width,weight,para):#计算米数，四舍五入
    return int(weight/width/para[0]/para[1]*para[2]+0.5)

class Interval():

    def __init__(self,left,right):
        self.left=float(left)#左边界
        self.right=float(right)#右边界

class Need():

    def __init__(self,width,weight,para):
        self.width=float(width)#需求宽度
        self.weight=float(weight)#需求重量
        self.length=cal_length(self.width,self.weight,para)#需求长度
        self.lengthscale=Interval(self.length,self.length)#需求米数范围
        self.left=0#需求左溢短差
        self.right=0#需求右溢短差
    
class Roll():

    def __init__(self,width,weight,id,type,neg,para,iron,magnet,card):
        self.widthscale=Interval(width,width)#母卷宽度范围
        self.width=float(width)#母卷宽度
        self.weight=float(weight)#母卷重量
        self.length=cal_length(self.width,self.weight,para)#母卷长度
        self.id=id#母卷卷号
        self.type=type#母卷类型——毛边卷、切边卷、库存
        self.iron=iron#铁损
        self.magnet=magnet#磁感
        self.card=card#牌号

class Bar():#客户定的边条规格

    def __init__(self,width,weight,para,sh):
        self.width=float(width)#边条宽度
        self.weight=float(weight)#边条重量
        self.length=cal_length(self.width,self.weight,para)#边条长度
        self.sym=sh#边条符号

class Bar_no_client():#非客户定的边条规格

    def __init__(self,width,sh):
        self.width=float(width)#边条宽度
        self.sym=sh#边条符号

def get_side_bar(SIDE_BAR_STR):
    SIDE_BAR_WIDTH = []
    if int(SIDE_BAR_STR[:1]) == 0:
        SIDE_BAR_WIDTH = []
        return SIDE_BAR_WIDTH
    else:
        if "," in SIDE_BAR_STR:
            SIDE_BAR_WIDTH = SIDE_BAR_STR.split(",")
        elif "，" in SIDE_BAR_STR:
            SIDE_BAR_WIDTH = SIDE_BAR_STR.split("，")
    SIDE_BAR_WIDTH = list(map(int, SIDE_BAR_WIDTH))
    return SIDE_BAR_WIDTH

def get_project(filename,pos,neg,Need_encoding,para):#获取需求项目规格
    project_simple_list = []#项目符号
    sidebar_simple_list = []#边条符号
    mark=0
    sidebar=[]
    if filename.split("/")[-1].split(".")[-1] == "csv":#读取csv和excel文件
        response=[]
        tempfile=csv.reader(open(filename,'r',encoding=Need_encoding))
        templist=[]
        flag=0
    else:
        response=[]
        df=pd.read_excel(filename,header = None)
        df_na = df.fillna('',  inplace=False)
        rows = df.index
        tempfile = []
        for i in range(len(rows)):
            tempfile.append(df_na.loc[i].values.tolist())
        templist=[]
        flag=0
    for item in tempfile:#遍历文件每一行
        #print(item[0])
        if item[0]=='宽度' or item[0]=='宽左':#标题栏
            if flag==0:#是不是首项目or首边条，不用添加上一个项目
                flag=1
            else:
                if mark==0:#项目结束
                    response.append(templist)
                    templist=[]
                else:#边条结束
                    sidebar.append(templist)
                    templist=[]
        elif str(item[0]).isdigit() == False:#非数字，项目名
            if str(item[0]).split('）')[0] == str(item[0]):#用了英文括号
                if len(str(item[0]).strip().split('(')[0]) == 2:#非项目名，而是边条
                    sh = str(item[0]).split(')')[0].split('(')[1]#边条符号
                    sidebar_simple_list.append(sh)
                    if mark==0:
                        mark=1
                        response.append(templist)
                        templist=[]
                        flag=0
                else:  
                    ch = str(item[0]).split(')')[0].split('(')[1]#项目符号
                    project_simple_list.append(ch)
            else:
                if len(str(item[0]).strip().split('（')[0]) == 2:#非项目名，而是边条
                    sh = str(item[0]).split('）')[0].split('（')[1]#边条符号
                    sidebar_simple_list.append(sh)
                    if mark==0:
                        mark=1
                        response.append(templist)
                        templist=[]
                        flag=0
                else:  
                    ch = str(item[0]).split('）')[0].split('（')[1]#项目符号
                    project_simple_list.append(ch)
        else:#是数字
            if mark==0:#新需求
                need=Need(item[0],item[1],para)
                if neg>0 or pos<0:
                    need.lengthscale.right=need.length*(1+pos)
                    need.length=need.length*(1+neg)
                    need.lengthscale.left=need.length
                    need.left=0
                    need.right=need.lengthscale.right-need.lengthscale.left
                elif neg<=0 and pos>=0:
                    need.lengthscale.left=need.length*(1+neg)
                    need.lengthscale.right=need.length*(1+pos)

                    need.left=need.length*neg
                    need.right=need.length*pos

                templist.append(need)
            else:#新边条
                bar=Bar(item[0],item[1],para,sh)#左边界，右边界、参数、符号
                templist.append(bar)
            
    #返回项目信息、项目符号、客户边条信息、边条符号、无客户边条信息
    return response, project_simple_list, sidebar,sidebar_simple_list,templist

def get_storage(filename,thread,bar,neg,Roll_encoding,para):#获取母卷规格
    if filename.split("/")[-1].split(".")[-1] == "csv":#读取csv和excel文件
        response=[]
        tempfile=csv.reader(open(filename,'r',encoding=Roll_encoding))
        flag=0
    else:
        response=[]
        df=pd.read_excel(filename,header = None)
        df_na = df.fillna('',  inplace=False)
        rows = df.index
        tempfile = []
        for i in range(len(rows)):
            tempfile.append(df_na.loc[i].values.tolist())
        flag=0
    for item in tempfile:
        if flag==0: #第一行
            flag=1
        else:
            roll=Roll(item[3],item[4],item[2],item[0],neg,para,item[5],item[6],item[1])#新母卷
            roll.widthscale.left=roll.width-thread[roll.type].right#减去边条
            roll.widthscale.right=roll.width-thread[roll.type].left
            if roll.type=="毛边卷":#毛边卷还要减去无客户边条，注意这里的bar已经是输入文件里边条的两倍
                roll.widthscale.left=roll.widthscale.left-bar.right
                roll.widthscale.right=roll.widthscale.right-bar.left
            response.append(roll)

    #返回母卷信息
    return response

def cal_weight(width,length,para):#计算重量
    return length*width*para[0]*para[1]/para[2]

def inscale(a,b):#判断a值是否在b区间内
    if a>=int(b.left) and a<=int(b.right):
        return True
    else:
        return False

def roll_satisfy(root_length,cut_length,min_length):#判断母卷切割后是否全部用完or满足最短米数
    #if root_length-cut_length>=min_length or (cut_length>=root_length-dist and cut_length<=root_length):
    if root_length-cut_length>=min_length or root_length-cut_length==0:
        return True
    else:
        return False

def need_satisfy(root_length,cut_length,left_length,right_length,min_length):#判断需求切割后是否恰好满足or满足最短米数or满足溢短差
    length_scale=Interval(root_length+left_length,root_length+right_length)
    if root_length-cut_length>=min_length or inscale(cut_length,length_scale):
        return True
    else:
        return False

def remain_process(remain_width,remain_min):#利处理余材
    n=int(remain_width/10)
    ans=[]
    if n*10>=remain_min:
        ans.append(n*10)
    return ans

def direct_match(project,storage,para,min_length,plan,sym,idlist,rollindex,prolist,record,step):#宽度直接匹配

    fneed=[]#分配完的需求

    total=0#分配的重量

    for item in project:#对每一个主项目需求

        froll=[]#分配完的母卷
        storage.sort(key=lambda x:(x.width,str(x.id)),reverse=True)#母卷按照宽度、长度和id号降序排序

        for roll in storage:#对于每一个母卷

            if inscale(item.width,roll.widthscale):#需求宽度在母卷宽度范围内
                print(f'宽度匹配:{item.width}')
                if roll_satisfy(roll.length,item.length,min_length):#需求精准分配，满足约束条件
                    print("step 1:")
                    content={}
                    content['width']=[item.width,]
                    content['length']=item.length

                    content['symbol']=[sym['项目'][0],]

                    plan[roll.id].append(content)#母卷分配情况

                    print(contents)

                    #记录
                    temprecord={}
                    temprecord['roll']=roll
                    temprecord['content']=content
                    record[step].append(temprecord)


                    prolist[0][str(item.width)].append((roll.id,content['length']))#需求分配情况

                    for a in range(rollindex,len(idlist)):#调整母卷顺序
                        if idlist[a]==roll.id:
                            temp=idlist[a]
                            idlist[a]=idlist[rollindex]
                            idlist[rollindex]=temp
                            rollindex=rollindex+1
                            break

                    total=total+cal_weight(item.width,item.length,para)#计算重量

                    fneed.append(item)#需求完成

                    if roll.length-item.length<min_length:
                        froll.append(roll)#母卷完成
                    else:
                        roll.length=roll.length-item.length#母卷裁剪
                    break#需求分配完了，换下一个需求

                if need_satisfy(item.length,roll.length,item.left,item.right,min_length)==True:#母卷全分配
                    print("step 2:")
                    content={}
                    content['width']=[item.width,]
                    content['length']=roll.length

                    content['symbol']=[sym['项目'][0],]

                    plan[roll.id].append(content)#母卷分配情况

                    print(content)

                    #记录
                    temprecord={}
                    temprecord['roll']=roll
                    temprecord['content']=content
                    record[step].append(temprecord)

                    prolist[0][str(item.width)].append((roll.id,content['length']))#需求分配情况

                    for a in range(rollindex,len(idlist)):#调整母卷顺序
                        if idlist[a]==roll.id:
                            temp=idlist[a]
                            idlist[a]=idlist[rollindex]
                            idlist[rollindex]=temp
                            rollindex=rollindex+1
                            break

                    total=total+cal_weight(item.width,roll.length,para)#计算重量

                    froll.append(roll)#母卷完成

                    if item.length-roll.length<min_length:
                        fneed.append(item)
                        break
                    else:
                        item.length=item.length-roll.length
                        item.lengthscale.left=item.length+item.left
                        item.lengthscale.right=item.length+item.right
                        continue
                
                #需求无法精准分配，母卷也无法全分配，判断是否能满足溢短差
                if item.lengthscale.right<roll.length:
                    temp=item.lengthscale.right
                else:
                    temp=roll.length
                #for i in range(int(item.lengthscale.left),int(temp)+1):
                for i in range(int(max(min_length,item.lengthscale.left)),int(temp)+1):
                #for i in range(int(max(min_length,item.lengthscale.left)),int(temp)+1):#是否能找到使需求满足溢短差的长度
                    if roll_satisfy(roll.length,i,min_length):
                        print("step 3:")
                        content={}
                        content['width']=[item.width,]
                        content['length']=i

                        content['symbol']=[sym['项目'][0],]

                        plan[roll.id].append(content)#母卷分配情况

                        print(content)

                        #记录
                        temprecord={}
                        temprecord['roll']=roll
                        temprecord['content']=content
                        record[step].append(temprecord)

                        prolist[0][str(item.width)].append((roll.id,content['length']))#需求分配情况

                        for a in range(rollindex,len(idlist)):#调整母卷顺序
                            if idlist[a]==roll.id:
                                temp=idlist[a]
                                idlist[a]=idlist[rollindex]
                                idlist[rollindex]=temp
                                rollindex=rollindex+1
                                break

                        total=total+cal_weight(item.width,i,para)#计算重量

                        fneed.append(item)#需求完成


                        if roll.length-i<min_length:
                            froll.append(roll)#母卷完成
                        else:
                            roll.length=roll.length-i#母卷裁剪
                        break#需求完成，不用再找切割长度
                
                if item in fneed:#需求完成
                    break
                else:#无法使需求满足溢短差，判断是否能使需求满足最短米数
                    #for i in range(int(item.length-min_length),0,-1):
                    for i in range(int(item.length-min_length),min_length,-1):#分配能分配的最大米数，需求未完成
                    #for i in range(min_length,int(item.length-min_length)+1):#需求满足最小米数的分配,在区间（0，需求米数-最短米数）中找到满足母卷的切割长度
                        if roll_satisfy(roll.length,i,min_length):
                            print("step 4:")
                            content={}
                            content['width']=[item.width,]
                            content['length']=i

                            content['symbol']=[sym['项目'][0],]

                            plan[roll.id].append(content)#母卷分配情况

                            print(content)

                            #记录
                            temprecord={}
                            temprecord['roll']=roll
                            temprecord['content']=content
                            record[step].append(temprecord)

                            prolist[0][str(item.width)].append((roll.id,content['length']))#需求分配情况

                            for a in range(rollindex,len(idlist)):#调整母卷顺序
                                if idlist[a]==roll.id:
                                    temp=idlist[a]
                                    idlist[a]=idlist[rollindex]
                                    idlist[rollindex]=temp
                                    rollindex=rollindex+1
                                    break

                            total=total+cal_weight(item.width,i,para)#计算重量

                            item.length=item.length-i#更新需求
                            item.lengthscale.left=item.length+item.left
                            item.lengthscale.right=item.length+item.right

                            if roll.length-i<min_length:
                                froll.append(roll)#母卷完成
                            else:
                                roll.length=roll.length-i#母卷裁剪
                            break
        
        storage=[x for x in storage if x not in froll]#更新库存
    
    project=[x for x in project if x not in fneed]#更新需求
    data={
        'project':project,
        'storage':storage,
        'plan':plan,
    }
    return data,total,rollindex

def used_roll_satisfy(sorted_storage,roll,templist,cut_length,shortneed,tempdic,min_length):

    if int((shortneed.length-cut_length)/tempdic[str(shortneed.width)]+0.5)<min_length:#下一卷的切割长度不能小于最短米数
        return False

    flag=0
    for need in templist:#下一个母卷全分配
        if need_satisfy(need.length-cut_length*tempdic[str(need.width)],roll.length*tempdic[str(need.width)],need.left,need.right,min_length)==False:
            flag=1
            break
    if flag==0:
        return True
     
    flag=0
    cut_length_next=int((shortneed.length-cut_length)/tempdic[str(shortneed.width)]+0.5)
    for need in templist:
        if need_satisfy(need.length-cut_length*tempdic[str(need.width)],tempdic[str(need.width)]*cut_length_next,need.left,need.right,min_length)==False:
            flag=1
            break
    if flag==0:
        return True

    interval=copy.deepcopy(shortneed.lengthscale)#获取最短需求的米数范围
    interval.left=interval.left/tempdic[str(shortneed.width)]-cut_length#更新米数范围
    interval.right=interval.right/tempdic[str(shortneed.width)]-cut_length
    
    for i in range(int(max(min_length,interval.left)),int(interval.right)):#满足最短需求溢短差
        if roll_satisfy(roll.length,i,min_length):#母卷满足要求
            flag=1#标识组合是否满足母卷条件

            for one in templist:
                if need_satisfy(one.length,tempdic[str(one.width)]*i,one.left,one.right,min_length)==False:#母卷不满足
                    flag=0
                    break

            if flag==1:
                return True
            
    return False

def used_cut(sorted_storage,project,roll,curroll,froll,fneed,maxlist,maxsum,para,min_length,plan,remain_min,sym,length_difference,prolist,record,step):

    for one in maxlist:
        print(one.width,end=' ')
                
    print()
    total=0

    tempdic={}#存需求在组合中出现的次数
    templist=[]#存不重复的需求

    for one in maxlist:#初始化tempdic和templist
        if one not in templist:
            templist.append(one)
            tempdic[str(one.width)]=0

    for one in maxlist:#计算组合内需求出现的次数
        tempdic[str(one.width)]=tempdic[str(one.width)]+1

    shortneed=maxlist[0]#找出切割长度最短的需求
    for tempitem in maxlist:
        if tempitem.length/tempdic[str(tempitem.width)]<shortneed.length/tempdic[str(shortneed.width)]:
            shortneed=tempitem

    interval=copy.deepcopy(shortneed.lengthscale)#获取最短需求的米数范围
    num=tempdic[str(shortneed.width)]#最短需求出现的次数

    print("cutlength:"+str(int(shortneed.length/num+0.5)))#该组合最短需求的切割长度

    if shortneed.length/num<min_length:#切割长度小于最短米数
        print("#########return 1")
        return -1,total#无效组合

    tempflag=0
    cut_length=int(shortneed.length/num+0.5)#切割长度四舍五入

    for one in maxlist:#需求间长度差>=指定值,对于组合内每个需求，如果不是准确切割 and 不是满足溢短差 and 切割后长度<指定值
        if inscale(tempdic[str(one.width)]*cut_length,one.lengthscale)==False and one.length-tempdic[str(one.width)]*cut_length<length_difference:
            #print(one.width)
            tempflag=1
            break

    print("tempflag:"+str(tempflag))
    if tempflag==1:
        print("#########return 2")
        return -1,total#无效组合

    interval.left=interval.left/num#更新米数范围
    interval.right=interval.right/num

    print("shortneed:"+str(shortneed.length)+' '+str(num))

    print("roll:"+str(roll.length))

    if need_satisfy(shortneed.length,roll.length*num,shortneed.left,shortneed.right,min_length)==True:#母卷全分配
        print("used step 1:")
        flag=1#标识组合是否满足母卷条件

        for one in templist:
            if need_satisfy(one.length,tempdic[str(one.width)]*roll.length,one.left,one.right,min_length)==False:#母卷不满足
                flag=0
                break

        if shortneed.length-roll.length*num>=min_length and curroll in sorted_storage:
            print("#########return 3")
            return -1,total

        print("flag:"+str(flag))

        if flag==1:#所有需求满足要求

            if used_roll_satisfy(sorted_storage,curroll,templist,roll.length,shortneed,tempdic,min_length)==True:
                content={}
                content['width']=[]
                content['length']=roll.length
                content['symbol']=[]
                froll.append(roll)
                done=0
                for item in maxlist:
                    content['width'].append(item.width)#需求宽度存入方案

                    content['symbol'].append(sym['项目'][0])

                    total=total+cal_weight(item.width,content['length'],para)

                    if item.length-content['length']<min_length:#更新需求
                        fneed.append(item)
                        done=1
                    else:
                        item.length=item.length-content['length']
                        item.lengthscale.left=item.length+item.left
                        item.lengthscale.right=item.length+item.right

                for width in content['width']:
                    prolist[0][str(width)].append((roll.id,content['length']))#需求分配情况

                remainlist=remain_process(roll.widthscale.right-maxsum,remain_min)#分配余材

                for width in remainlist:
                    content['width'].append(width)
                    content['symbol'].append(sym['余材'])

                width_sort(content['width'],content['symbol'])

                plan[roll.id].append(content)#存入方案

                print(content)

                for x in fneed:
                    project.remove(x)

                #记录
                temprecord={}
                temprecord['roll']=roll
                temprecord['content']=content
                record[step].append(temprecord)

                print("used 1 cut")

                if done==0:
                    print("#########return 4")
                    return 0,total#没分配完，母卷用完了
                else:
                    print("#########return 5")
                    return 1,total#分配完，母卷也用完

    if roll_satisfy(roll.length,cut_length,min_length)==True:#最短需求满足
        print("used step 2:")
        flag=1#标识组合是否满足母卷条件

        for one in templist:
            if need_satisfy(one.length,tempdic[str(one.width)]*cut_length,one.left,one.right,min_length)==False:#母卷不满足         
                flag=0
                break

        print("flag:"+str(flag))
        
        if flag==1:#所有需求满足要求

            content={}
            content['width']=[]
            content['length']=cut_length
            content['symbol']=[]
           
            if roll.length-content['length']<min_length:
                froll.append(roll)
                used=0
            else:
                roll.length=roll.length-content['length']
                used=1

            for item in maxlist:
                content['width'].append(item.width)#需求宽度存入方案

                content['symbol'].append(sym['项目'][0])

                total=total+cal_weight(item.width,content['length'],para)#计算重量

                if item.length-content['length']<min_length:#更新需求
                    fneed.append(item)
                    print(str(item.width)+' finish')
                else:
                    item.length=item.length-content['length']
                    item.lengthscale.left=item.length+item.left
                    item.lengthscale.right=item.length+item.right

            for width in content['width']:
                prolist[0][str(width)].append((roll.id,content['length']))#需求分配情况

            remainlist=remain_process(roll.widthscale.right-maxsum,remain_min)#分配余材
            for width in remainlist:
                content['width'].append(width)
                content['symbol'].append(sym['余材'])

            width_sort(content['width'],content['symbol'])

            plan[roll.id].append(content)#存入方案

            #记录
            temprecord={}
            temprecord['roll']=roll
            temprecord['content']=content
            record[step].append(temprecord)

            print(content)

            for x in fneed:
                project.remove(x)

            for x in project:
                print(x.width,end=' ')

            print("used 2 cut")

            if used==0:
                print("#########return 6")
                return 1,total#分配完，母卷也用完
            else:
                print("#########return 7")
                return 2,total#分配完，母卷没用完

    tempflag=0
    for i in range(int(max(min_length,interval.left)),int(interval.right)):#满足最短需求溢短差
        if roll_satisfy(roll.length,i,min_length):#母卷满足要求
            print("used step 3:")
            flag=1#标识组合是否满足母卷条件

            for one in templist:
                if need_satisfy(one.length,tempdic[str(one.width)]*i,one.left,one.right,min_length)==False:#母卷不满足
                    flag=0
                    break

            print("flag:"+str(flag))

            if flag==1:#所有需求满足要求
                tempflag=1
                content={}
                content['width']=[]
                content['length']=i
                content['symbol']=[]

                if roll.length-content['length']<min_length:#更新母卷
                    froll.append(roll)
                    used=0
                else:
                    roll.length=roll.length-content['length']
                    used=1

                for item in maxlist:
                    content['width'].append(item.width)#需求宽度存入方案

                    content['symbol'].append(sym['项目'][0])

                    total=total+cal_weight(item.width,content['length'],para)#计算重量

                    if item.length-content['length']<min_length:#更新需求
                        fneed.append(item)
                    else:
                        item.length=item.length-content['length']
                        item.lengthscale.left=item.length+item.left
                        item.lengthscale.right=item.length+item.right

                for width in content['width']:
                    prolist[0][str(width)].append((roll.id,content['length']))#需求分配情况
                
                remainlist=remain_process(roll.widthscale.right-maxsum,remain_min)#分配余材
                for width in remainlist:
                    content['width'].append(width)
                    content['symbol'].append(sym['余材'])
                
                width_sort(content['width'],content['symbol'])
                
                plan[roll.id].append(content)#存入方案

                #记录
                temprecord={}
                temprecord['roll']=roll
                temprecord['content']=content
                record[step].append(temprecord)

                print(content)

                for x in fneed:
                    project.remove(x)

                print("used 3 cut")
                
                if used==0:
                    print("#########return 8")
                    return 1,total#分配完，母卷也用完
                else:
                    print("#########return 9")
                    return 2,total#分配完，母卷没用完
    print("#########return 10")
    return -1,total

def width_match(project,otherproject,storage,para,min_length,plan,remain_min,sym,method,length_difference,prolist,idlist,rollindex,sorted_storage,left_cut,record,step):#基于宽度组合匹配
    storage.sort(key=lambda x:(x.widthscale.right,str(x.id)),reverse=True)#母卷按照宽度、长度、id降序排序

    total=0#分配重量
    total2=0

    froll=[]#分配完的母卷

    left=0#组合是否没分配完，有剩余
    leftneed=[]#剩余的宽度组合
    leftmode=0

    used=0#上一卷是否有剩余

    same=0

    lastwidth=[]
    lastneed=[]

    flag_not_done=0
    used_need=[]

    
    for roll in storage:#遍历母卷
        templen=0#用来判断母卷是不是做了变动
        setlist=[]#无效组合

        while 1:#母卷一直做宽度匹配，直到用完或没有合适的宽度组合
            if roll in froll:#母卷用完
                break
            if templen==roll.length:#母卷无变动，当前组合认定为无效组合
                setlist.append(maxlist)
            if templen!=roll.length:#母卷变动
                templen=roll.length

            countdic={}#存组合里需求出现的次数
            for obj in project:
                countdic[str(obj.width)]=0
                     
            fneed=[]#分配完的需求

            project.sort(key=lambda x:x.width,reverse=True)#需求按宽度从大到小排序
            #itemlist=project#存所有项目

            maxnum=0#组合内需求个数的最大值
            if method==0:
                tempsum=0
                c=0
                for i in range(len(project)-1,-1,-1):
                    if tempsum>=roll.widthscale.right:
                        break
                    tempsum=tempsum+project[i].width
                    c=c+1
                if tempsum!=0 and tempsum<roll.widthscale.right:
                    maxnum=int(roll.widthscale.right/tempsum+0.5)*c
                else:
                    maxnum=c

                maxnum=int(maxnum/2+0.5)
            elif method==1:#平均数——母卷宽度范围右边界/需求宽度平均数
                tempsum=0
                c=0
                for obj in project:
                    if obj.width<=roll.widthscale.right:
                        tempsum=tempsum+obj.width
                        c=c+1
                if c!=0:
                    avg=tempsum/c
                    maxnum=int(roll.widthscale.right/avg)
            elif method==2:#中位数——母卷宽度范围右边界/需求宽度中位数
                templist3=[]
                for obj in project:
                    if obj.width<=roll.widthscale.right:
                        templist3.append(obj)
                if len(templist3)==0:
                    break
                tempmark=int(len(templist3)/2)
                if len(templist3)%2==0:
                    mid=(templist3[tempmark].width+templist3[tempmark-1].width)/2
                else:
                    mid=templist3[tempmark].width
                maxnum=int(roll.widthscale.right/mid)
            elif method==3:#平均数+1
                tempsum=0
                c=0
                for obj in project:
                    if obj.width<=roll.widthscale.right:
                        tempsum=tempsum+obj.width
                        c=c+1
                if c!=0:
                    avg=tempsum/c
                    maxnum=int(roll.widthscale.right/avg)+1
            elif method==4:#平均数-1
                tempsum=0
                c=0
                for obj in project:
                    if obj.width<=roll.widthscale.right:
                        tempsum=tempsum+obj.width
                        c=c+1
                if c!=0:
                    avg=tempsum/c
                    maxnum=int(roll.widthscale.right/avg)-1
            elif method==5:#中位数+1
                templist3=[]
                for obj in project:
                    if obj.width<=roll.widthscale.right:
                        templist3.append(obj)
                if len(templist3)==0:
                    break
                tempmark=int(len(templist3)/2)
                if len(templist3)%2==0:
                    mid=(templist3[tempmark].width+templist3[tempmark-1].width)/2
                else:
                    mid=templist3[tempmark].width
                maxnum=int(roll.widthscale.right/mid)+1
            elif method==6:#中位数-1
                templist3=[]
                for obj in project:
                    if obj.width<=roll.widthscale.right:
                        templist3.append(obj)
                if len(templist3)==0:
                    break
                tempmark=int(len(templist3)/2)
                if len(templist3)%2==0:
                    mid=(templist3[tempmark].width+templist3[tempmark-1].width)/2
                else:
                    mid=templist3[tempmark].width
                maxnum=int(roll.widthscale.right/mid)-1


            i=int(roll.widthscale.left/project[0].width)
            maxsum=0#宽度之和最大值
            maxlist=[]#最大宽度组合
            minsum=float('inf')#宽度之和最小值

            maxsim=0

            found=0

            print(roll.id,end=' ')
            print(left)
            print('used:'+str(used))

            if left==1:#上一卷的连续组合可能不是最后一个配刀
                leftwidth=[]
                for x in leftneed:
                    leftwidth.append(x.width)
                leftwidth.extend(remain_process(roll.widthscale.right-sum([x.width for x in leftneed]),remain_min))

                print(leftwidth)
                print(plan[lastroll][-1]['width'])

            if flag_not_done==1:
                if inscale(need1.width+need2.width,roll.widthscale)==False:
                    flag_not_done=0

            if flag_not_done==1:
                for index in range(len(otherproject)):
                    for p in otherproject[index]:
                        if p.width==need2.width and p not in used_need:
                            maxsum=need1.width+p.width
                            maxlist=[need1,p]
                            used_need.append(p)
                            break
                    if maxsum!=0:
                        break
                if maxsum==0:
                    flag_not_done=0
                    used_need=[]

            if left==1 and roll.id not in sorted_storage and plan[lastroll][-1]['width']==leftwidth:#如果上一个母卷最后一个组合没分配完，且当前母卷和其他母卷没有连续关系
                tempsum=sum([x.width for x in leftneed])
                if inscale(tempsum,roll.widthscale):#组合宽度之和在母卷可用宽度范围内，则直接指定最大宽度组合为该组合
                    maxsum=tempsum
                    maxlist=leftneed
            if maxsum==0:
                if left==1:
                    left=0

                combinelist=[]
                combinelist.extend(project)
                for x in lastneed:
                    if x not in combinelist:
                        for index in range(len(otherproject)):
                            if x in otherproject[index]:
                                combinelist.append(x)
                                break

                print("combinelist:",end='')
                for x in combinelist:
                    print(x.width,end=' ')
                print()

                while 1:
                    for subset in combinations_with_replacement(combinelist,i):#宽度所有组合
                        if list(subset) in setlist:#是否是无效组合
                            continue


                        tempflag=0
                        for obj in subset:
                            if obj in project:
                                tempflag=1
                                break
                        if tempflag==0:
                            continue

                        for obj in countdic:
                            countdic[obj]=0

                        otherdic={}

                        for x in subset:
                            if x not in project:
                                otherdic[str(x.width)]=0

                        flag=0
                        for obj in subset:
                            if obj in project:
                                if countdic[str(obj.width)]>=3:#同一个需求在一个组合里不允许出现3次以上
                                    flag=1
                                    break
                                countdic[str(obj.width)]=countdic[str(obj.width)]+1
                            else:
                                if otherdic[str(obj.width)]>=3:#同一个需求在一个组合里不允许出现3次以上
                                    flag=1
                                    break
                                otherdic[str(obj.width)]=otherdic[str(obj.width)]+1
                        if flag==1:
                            continue
                                
                        tempsum=sum([x.width for x in subset])#求宽度之和
                        if inscale(tempsum,roll.widthscale) and found==0:
                            if tempsum>maxsum:#宽度之和更大
                                #for x in subset:
                                    #print(x.width,end=' ')
                                #print()
                                maxsum=tempsum
                                maxlist=list(subset)
                                maxsim=0
                                #print('maxsum:'+str(maxsum))
                            elif tempsum==maxsum:#宽度之和相等
                                tempsim=0
                                tempwidth=[]

                                for x in subset:
                                    tempwidth.append(x.width)

                                for x in lastwidth:
                                    if x in tempwidth:
                                        tempsim=tempsim+1

                                """ for tempneed in lastneed:
                                    if tempneed in subset:
                                        tempsim=tempsim+1 """
                                if tempsim>maxsim:
                                    maxlist=list(subset)
                                    maxsim=tempsim

                                    """ print("templist:",end=' ')
                                    print(templist)

                                    print("maxsim:"+str(maxsim))

                                    print(lastwidth)
                                    print("与上一个组合相似度更高哦！") """

                        if inscale(tempsum,roll.widthscale):#判断母卷是不是能全部分配

                            tempdic={}#存需求在组合中出现的次数
                            templist=[]#存不重复的需求

                            for one in subset:#初始化tempdic和templist
                                if one not in templist:
                                    templist.append(one)
                                    tempdic[str(one.width)]=0

                            for one in subset:#计算组合内需求出现的次数
                                tempdic[str(one.width)]=tempdic[str(one.width)]+1

                            tempshortneed=subset[0]#找出切割长度最短的需求
                            for tempitem in subset:
                                if tempitem.length/tempdic[str(tempitem.width)]<tempshortneed.length/tempdic[str(tempshortneed.width)]:
                                    tempshortneed=tempitem

                            length_scale=Interval((tempshortneed.length+tempshortneed.left)/tempdic[str(tempshortneed.width)],(tempshortneed.length+tempshortneed.right)/tempdic[str(tempshortneed.width)])


                            if inscale(roll.length,length_scale):#母卷能全部分配完且满足需求
                                if found==0:
                                    found=1
                                    maxsum=tempsum
                                    maxlist=list(subset)
                                    maxsim=0
                                elif found==1:
                                    if tempsum>maxsum:
                                        maxsum=tempsum
                                        maxlist=list(subset)
                                        maxsim=0
                                    elif tempsum==maxsum:
                                        tempsim=0
                                        tempwidth=[]

                                        for x in subset:
                                            tempwidth.append(x.width)

                                        for x in lastwidth:
                                            if x in tempwidth:
                                                tempsim=tempsim+1

                                        """ for tempneed in lastneed:
                                            if tempneed in subset:
                                                tempsim=tempsim+1 """
                                        if tempsim>maxsim:
                                            maxlist=list(subset)
                                            maxsim=tempsim


                        if tempsum<minsum:#求当前所有组合宽度的最小和
                            minsum=tempsum

                    if minsum>=roll.widthscale.right or i >= maxnum:#母卷已经满足不了更大的宽度
                        break
                    else:
                        minsum=float('inf')
                        i=i+1

            if left==1 and maxsum==0:#剩余组合无效
                left=0 #取消剩余组合，继续找新的组合
                continue

            if used==1 and maxsum!=0 and roll.id not in sorted_storage:#上一卷没用完
                response,d=used_cut(sorted_storage,project,usedroll,roll,froll,fneed,maxlist,maxsum,para,min_length,plan,remain_min,sym,length_difference,prolist,record,step)
                print("response:"+str(response))
                
                if response==-1 or response==2:#上一卷不可分配 or 分配完，母卷没用完
                    total=total+d
                    continue
                elif response==0:#没分配完，母卷用完了
                    used=0
                    left=1
                    leftneed=maxlist
                    lastroll=usedroll.id
                    setlist=[]
                    same=1
                    total=total+d
                    continue
                elif response==1:#分配完，母卷也用完
                    used=0
                    setlist=[]
                    total=total+d
                    continue

            if maxsum==0:#无有效组合，换卷
                if used==1:#上一卷剩余无法分配，直接开始这一卷
                    used=0
                    setlist=[]
                    continue
                if roll.id in idlist[:rollindex]:#这一卷有剩余
                    used=1
                    usedroll=roll
                break#换卷
            
            print(maxnum)
            if maxsum!=0:#有最优宽度组合

                print(roll.id)

                print('found:'+str(found))#是否母卷全部分配完

                print('left:'+str(left))#是否是剩余组合

                print("flag_not_done:"+str(flag_not_done))

                for one in maxlist:
                    print(one.width,end=' ')
                
                print()

                tempdic={}#存需求在组合中出现的次数
                templist=[]#存不重复的需求

                for one in maxlist:#初始化tempdic和templist
                    if one not in templist:
                        templist.append(one)
                        tempdic[str(one.width)]=0

                for one in maxlist:#计算组合内需求出现的次数
                    tempdic[str(one.width)]=tempdic[str(one.width)]+1

                shortneed=maxlist[0]#找出切割长度最短的需求
                for tempitem in maxlist:
                    if tempitem.length/tempdic[str(tempitem.width)]<shortneed.length/tempdic[str(shortneed.width)]:
                        shortneed=tempitem

                interval=copy.deepcopy(shortneed.lengthscale)#获取最短需求的米数范围
                num=tempdic[str(shortneed.width)]#最短需求出现的次数

                print("cutlength:"+str(int(shortneed.length/num+0.5)))#该组合最短需求的切割长度

                if shortneed.length/num<min_length:#切割长度小于最短米数
                    if left==1:
                        left=0#剩余组合无效
                    continue#组合无效

                tempflag=0
                cut_length=int(shortneed.length/num+0.5)#切割长度四舍五入

                for one in maxlist:#需求间长度差>=指定值,对于组合内每个需求，如果不是准确切割 and 不是满足溢短差 and 切割后长度<指定值
                    if inscale(tempdic[str(one.width)]*cut_length,one.lengthscale)==False and one.length-tempdic[str(one.width)]*cut_length<length_difference:
                        print(one.width)
                        tempflag=1
                        break

                print("tempflag:"+str(tempflag))
                if tempflag==1 and same==0:
                    if left==1:
                        left=0#剩余组合无效
                    for one in maxlist:
                        print(one.width,end=' ')
                        print(one.length,end=' ')
                        print(one.lengthscale.left,end=' ')
                        print(one.lengthscale.right)
                    continue


                interval.left=interval.left/num#更新米数范围
                interval.right=interval.right/num

                if need_satisfy(shortneed.length,roll.length*num,shortneed.left,shortneed.right,min_length)==True:#母卷全分配
                    print("step 1:")
                    flag=1#标识组合是否满足母卷条件

                    for one in templist:
                        if need_satisfy(one.length,tempdic[str(one.width)]*roll.length,one.left,one.right,min_length)==False:#母卷不满足
                            flag=0
                            break

                    print("flag:"+str(flag))

                    if flag==0:
                        for one in templist:
                            print(one.width,end=' ')
                            print(one.length,end=' ')
                            print(one.lengthscale.left,end=' ')
                            print(one.lengthscale.right)
                    
                    if flag==1:#所有需求满足要求
                        content={}
                        content['width']=[]
                        content['length']=roll.length
                        content['symbol']=[]
                        froll.append(roll)
                        done=0
                        for item in maxlist:
                            content['width'].append(item.width)#需求宽度存入方案

                            if item in project:

                                content['symbol'].append(sym['项目'][0])

                                total=total+cal_weight(item.width,roll.length,para)

                                prolist[0][str(item.width)].append((roll.id,content['length']))#需求分配情况

                            else:
                                for index in range(len(otherproject)):
                                    if item in otherproject[index]:
                                        content['symbol'].append(sym['项目'][index+1])

                                        total2=total2+cal_weight(item.width,content['length'],para)

                                        prolist[index+1][str(item.width)].append((roll.id,content['length']))

                                        break


                            if item.length-roll.length<min_length:#更新需求
                                fneed.append(item)
                                done=1
                            else:
                                item.length=item.length-roll.length
                                item.lengthscale.left=item.length+item.left
                                item.lengthscale.right=item.length+item.right

                        remainlist=remain_process(roll.widthscale.right-maxsum,remain_min)#分配余材

                        for width in remainlist:
                            content['width'].append(width)
                            content['symbol'].append(sym['余材'])

                        for a in range(rollindex,len(idlist)):#调整母卷顺序
                            if idlist[a]==roll.id:
                                temp=idlist[a]
                                idlist[a]=idlist[rollindex]
                                idlist[rollindex]=temp
                                rollindex=rollindex+1
                                break
                                
                        if left==1:#是剩余组合
                            left=0

                            width_sort(content['width'],content['symbol'])

                            plan[roll.id].insert(0,content)#与上一卷成连续关系

                            #记录
                            temprecord={}
                            temprecord['roll']=roll
                            temprecord['content']=content
                            record[step].append(temprecord)

                            sorted_storage.append(roll.id)#当前母卷已有连续关系

                            idlist.remove(roll.id)#改变当前母卷顺序，放在上一卷母卷的后面
                            idx=idlist.index(lastroll)
                            idlist.insert(idx+1,roll.id)

                            left_cut=left_cut+1#连续配刀数
                            print("连续")

                        elif same==1:
                            same=0

                            width_sort(content['width'],content['symbol'])

                            plan[roll.id].insert(0,content)

                            #记录
                            temprecord={}
                            temprecord['roll']=roll
                            temprecord['content']=content
                            record[step].append(temprecord)

                            sorted_storage.append(roll.id)#当前母卷已有连续关系

                            idlist.remove(roll.id)#改变当前母卷顺序，放在上一卷母卷的后面
                            idx=idlist.index(lastroll)
                            idlist.insert(idx+1,roll.id)

                            left_cut=left_cut+1#连续配刀数
                            print("连续")

                        else:
                            width_sort(content['width'],content['symbol'])

                            plan[roll.id].append(content)#存入方案

                            #记录
                            temprecord={}
                            temprecord['roll']=roll
                            temprecord['content']=content
                            record[step].append(temprecord)

                        print('done：'+str(done))

                        if done==0:#没分配完
                            left=1
                            leftneed=maxlist
                            lastroll=roll.id

                            print("没分配完")

                        print(content)

                        lastwidth=content['width']
            
                        project=[x for x in project if x not in fneed]#更新需求

                        for index in range(len(otherproject)):
                            otherproject[index]=[x for x in otherproject[index] if x not in fneed]

                        if len(maxlist)==2:

                            if maxlist[0] in fneed and maxlist[1] not in fneed and maxlist[1] in project:
                                flag_not_done=1
                                need1=maxlist[1]
                                need2=maxlist[0]
                                used_need=[]

                            elif maxlist[0] not in fneed and maxlist[1] in fneed and maxlist[0] in project:
                                flag_not_done=1
                                need1=maxlist[0]
                                need2=maxlist[1]
                                used_need=[]
                            
                            elif flag_not_done==1:
                                flag_not_done=0

                        lastneed=[]
                        lastneed.extend(maxlist)
                        tempwidth=[]
                        for x in lastneed:
                            if x.width not in tempwidth:
                                tempwidth.append(x.width)

                        for tempneed in project:
                            if tempneed not in lastneed and tempneed.width in tempwidth:
                                lastneed.append(tempneed)
                        
                        for index in range(len(otherproject)):
                            for tempneed in otherproject[index]:
                                if tempneed not in lastneed and tempneed.width in tempwidth:
                                    lastneed.append(tempneed)
                            

                        break#下一卷
                
                if roll_satisfy(roll.length,cut_length,min_length)==True:#最短需求满足
                    print("step 2:")
                    flag=1#标识组合是否满足母卷条件

                    for one in templist:
                        if need_satisfy(one.length,tempdic[str(one.width)]*cut_length,one.left,one.right,min_length)==False:#母卷不满足         
                            flag=0
                            break

                    print("flag:"+str(flag))

                    if flag==0:
                        for one in templist:
                            print(one.width,end=' ')
                            print(one.length,end=' ')
                            print(one.lengthscale.left,end=' ')
                            print(one.lengthscale.right)
                    
                    if flag==1:#所有需求满足要求
                        content={}
                        content['width']=[]
                        content['length']=cut_length
                        content['symbol']=[]
                        
                        if roll.length-content['length']<min_length:
                            froll.append(roll)
                        else:
                            roll.length=roll.length-content['length']

                        for item in maxlist:
                            content['width'].append(item.width)#需求宽度存入方案

                            if item in project:

                                content['symbol'].append(sym['项目'][0])

                                total=total+cal_weight(item.width,content['length'],para)

                                prolist[0][str(item.width)].append((roll.id,content['length']))#需求分配情况

                            else:
                                for index in range(len(otherproject)):
                                    if item in otherproject[index]:
                                        content['symbol'].append(sym['项目'][index+1])

                                        total2=total2+cal_weight(item.width,content['length'],para)

                                        prolist[index+1][str(item.width)].append((roll.id,content['length']))

                                        break

                            if item.length-content['length']<min_length:#更新需求
                                fneed.append(item)
                            else:
                                item.length=item.length-content['length']
                                item.lengthscale.left=item.length+item.left
                                item.lengthscale.right=item.length+item.right

                        remainlist=remain_process(roll.widthscale.right-maxsum,remain_min)#分配余材
                        for width in remainlist:
                            content['width'].append(width)
                            content['symbol'].append(sym['余材'])

                        for a in range(rollindex,len(idlist)):#调整母卷顺序
                            if idlist[a]==roll.id:
                                temp=idlist[a]
                                idlist[a]=idlist[rollindex]
                                idlist[rollindex]=temp
                                rollindex=rollindex+1
                                break
                        
                        if left==1:
                            left=0

                            width_sort(content['width'],content['symbol'])

                            plan[roll.id].insert(0,content)#与上一卷成联系关系

                            #记录
                            temprecord={}
                            temprecord['roll']=roll
                            temprecord['content']=content
                            record[step].append(temprecord)

                            sorted_storage.append(roll.id)#当前母卷已有连续关系
                            idlist.remove(roll.id)#将当前母卷排在上一卷的后面
                            idx=idlist.index(lastroll)
                            idlist.insert(idx+1,roll.id)
                            left_cut=left_cut+1#连续配刀数+1
                            print("连续")

                        elif same==1:
                            same=0

                            width_sort(content['width'],content['symbol'])

                            plan[roll.id].insert(0,content)

                            #记录
                            temprecord={}
                            temprecord['roll']=roll
                            temprecord['content']=content
                            record[step].append(temprecord)

                            sorted_storage.append(roll.id)#当前母卷已有连续关系

                            idlist.remove(roll.id)#改变当前母卷顺序，放在上一卷母卷的后面
                            idx=idlist.index(lastroll)
                            idlist.insert(idx+1,roll.id)

                            left_cut=left_cut+1#连续配刀数
                            print("连续")

                        else:
                            width_sort(content['width'],content['symbol'])

                            plan[roll.id].append(content)#存入方案

                            #记录
                            temprecord={}
                            temprecord['roll']=roll
                            temprecord['content']=content
                            record[step].append(temprecord)


                        print(content)

                        lastwidth=content['width']

                        project=[x for x in project if x not in fneed]#更新需求

                        for index in range(len(otherproject)):
                            otherproject[index]=[x for x in otherproject[index] if x not in fneed]

                        if len(maxlist)==2:

                            if maxlist[0] in fneed and maxlist[1] not in fneed and maxlist[1] in project:
                                flag_not_done=1
                                need1=maxlist[1]
                                need2=maxlist[0]
                                used_need=[]

                            elif maxlist[0] not in fneed and maxlist[1] in fneed and maxlist[0] in project:
                                flag_not_done=1
                                need1=maxlist[0]
                                need2=maxlist[1]
                                used_need=[]
                            
                            elif flag_not_done==1:
                                flag_not_done=0

                        lastneed=[]
                        lastneed.extend(maxlist)
                        tempwidth=[]
                        for x in lastneed:
                            if x.width not in tempwidth:
                                tempwidth.append(x.width)

                        for tempneed in project:
                            if tempneed not in lastneed and tempneed.width in tempwidth:
                                lastneed.append(tempneed)
                        
                        for index in range(len(otherproject)):
                            for tempneed in otherproject[index]:
                                if tempneed not in lastneed and tempneed.width in tempwidth:
                                    lastneed.append(tempneed)

                        continue

                tempflag=0
                #for i in range(int(interval.right),int(interval.left)):
                for i in range(int(max(min_length,interval.left)),int(interval.right)):#满足最短需求溢短差
                #for i in range(int(max(min_length,interval.left)),int(interval.right)):#找到既满足母卷又满足组合需求的分割长度
                    if roll_satisfy(roll.length,i,min_length):#母卷满足要求
                        print("step 3:")
                        flag=1#标识组合是否满足母卷条件

                        for one in templist:
                            if need_satisfy(one.length,tempdic[str(one.width)]*i,one.left,one.right,min_length)==False:#母卷不满足
                                flag=0
                                break

                        print("flag:"+str(flag))

                        if flag==0:
                            for one in templist:
                                print(one.width,end=' ')
                                print(one.length,end=' ')
                                print(one.lengthscale.left,end=' ')
                                print(one.lengthscale.right)
                
                        if flag==1:#所有需求满足要求
                            tempflag=1
                            content={}
                            content['width']=[]
                            content['length']=i
                            content['symbol']=[]

                            if roll.length-i<min_length:#更新母卷
                                froll.append(roll)
                            else:
                                roll.length=roll.length-i

                            for item in maxlist:
                                content['width'].append(item.width)#需求宽度存入方案

                                if item in project:

                                    content['symbol'].append(sym['项目'][0])

                                    total=total+cal_weight(item.width,content['length'],para)

                                    prolist[0][str(item.width)].append((roll.id,content['length']))#需求分配情况

                                else:
                                    for index in range(len(otherproject)):
                                        if item in otherproject[index]:
                                            content['symbol'].append(sym['项目'][index+1])

                                            total2=total2+cal_weight(item.width,content['length'],para)

                                            prolist[index+1][str(item.width)].append((roll.id,content['length']))

                                            break

                                if item.length-i<min_length:#更新需求
                                    fneed.append(item)
                                else:
                                    item.length=item.length-i
                                    item.lengthscale.left=item.length+item.left
                                    item.lengthscale.right=item.length+item.right
                            
                            remainlist=remain_process(roll.widthscale.right-maxsum,remain_min)#分配余材
                            for width in remainlist:
                                content['width'].append(width)
                                content['symbol'].append(sym['余材'])

                            for a in range(rollindex,len(idlist)):#调整母卷顺序
                                if idlist[a]==roll.id:
                                    temp=idlist[a]
                                    idlist[a]=idlist[rollindex]
                                    idlist[rollindex]=temp
                                    rollindex=rollindex+1
                                    break
                            
                            if left==1:#如果是剩余组合
                                left=0

                                width_sort(content['width'],content['symbol'])

                                plan[roll.id].insert(0,content)#与上一卷成连续关系

                                #记录
                                temprecord={}
                                temprecord['roll']=roll
                                temprecord['content']=content
                                record[step].append(temprecord)

                                sorted_storage.append(roll.id)#已有连续关系
                                idlist.remove(roll.id)#将当前母卷移到上一卷的后面
                                idx=idlist.index(lastroll)
                                idlist.insert(idx+1,roll.id)
                                left_cut=left_cut+1#连续配刀数+1
                                print("连续")

                            elif same==1:
                                same=0

                                width_sort(content['width'],content['symbol'])

                                plan[roll.id].insert(0,content)

                                #记录
                                temprecord={}
                                temprecord['roll']=roll
                                temprecord['content']=content
                                record[step].append(temprecord)

                                sorted_storage.append(roll.id)#当前母卷已有连续关系

                                idlist.remove(roll.id)#改变当前母卷顺序，放在上一卷母卷的后面
                                idx=idlist.index(lastroll)
                                idlist.insert(idx+1,roll.id)

                                left_cut=left_cut+1#连续配刀数
                                print("连续")

                            else:

                                width_sort(content['width'],content['symbol'])

                                plan[roll.id].append(content)#存入方案

                                #记录
                                temprecord={}
                                temprecord['roll']=roll
                                temprecord['content']=content
                                record[step].append(temprecord)


                            print(content)

                            lastwidth=content['width']

                            project=[x for x in project if x not in fneed]#更新需求

                            for index in range(len(otherproject)):
                                otherproject[index]=[x for x in otherproject[index] if x not in fneed]

                            if len(maxlist)==2:

                                if maxlist[0] in fneed and maxlist[1] not in fneed and maxlist[1] in project:
                                    flag_not_done=1
                                    need1=maxlist[1]
                                    need2=maxlist[0]
                                    used_need=[]

                                elif maxlist[0] not in fneed and maxlist[1] in fneed and maxlist[0] in project:
                                    flag_not_done=1
                                    need1=maxlist[0]
                                    need2=maxlist[1]
                                    used_need=[]
                                
                                elif flag_not_done==1:
                                    flag_not_done=0

                            lastneed=[]
                            lastneed.extend(maxlist)
                            tempwidth=[]
                            for x in lastneed:
                                if x.width not in tempwidth:
                                    tempwidth.append(x.width)

                            for tempneed in project:
                                if tempneed not in lastneed and tempneed.width in tempwidth:
                                    lastneed.append(tempneed)
                            
                            for index in range(len(otherproject)):
                                for tempneed in otherproject[index]:
                                    if tempneed not in lastneed and tempneed.width in tempwidth:
                                        lastneed.append(tempneed)

                            break

                if tempflag==0 and left==1:
                    if len(leftneed)==2 and leftmode==0:
                        mode_0_flag=0
                        for index in range(len(otherproject)):
                            for tempneed in otherproject[index]:
                                if tempneed.width==leftneed[0].width and tempneed not in used_need:
                                    leftneed[0]=tempneed
                                    used_need.append(tempneed)
                                    mode_0_flag=1
                                    break
                            if mode_0_flag==1:
                                break
                        if mode_0_flag==0:
                            leftmode=1
                            for tempneed in project:
                                if tempneed.width==leftneed[0].width:
                                    leftneed[0]=tempneed
                                    break
                    elif len(leftneed)==2 and leftmode==1:
                        mode_1_flag=0
                        for index in range(len(otherproject)):
                            for tempneed in otherproject[index]:
                                if tempneed.width==leftneed[1].width and tempneed not in used_need:
                                    leftneed[1]=tempneed
                                    used_need.append(tempneed)
                                    mode_1_flag=1
                                    break
                            if mode_1_flag==1:
                                break
                        if mode_1_flag==0:
                            left=0
                    else:
                        left=0
        if len(project)==0:
            break
                    
    storage=[x for x in storage if x not in froll]#更新库存
    data={
        'project':project,
        'storage':storage,
        'plan':plan,
        'otherproject':otherproject
    }
    return total2,data,total,rollindex,left_cut

def isoverlap(x,y):#判断两区间x、y是否相交
    if (x.right>=y.left and x.right<=y.right) or (y.right>=x.left and y.right<=x.right):
        return True
    else:
        return False

def scale_update(x,y):#返回两区间x、y的交集
    if x.left<y.left:
        a=y.left
    else:
        a=x.left

    if x.right<y.right:
        b=x.right
    else:
        b=y.right
    return Interval(a,b)

def length_match(project,storage,para,min_length,plan,remain_min,sym,method,otherproject,prolist,idlist,rollindex,record,step):#基于长度组合分配
    templen=-1#标识
    #for i in project:
        #print(f'{i.width}  {i.length}')
    cproject=copy.deepcopy(project)#项目副本
    total=0#主项目重量
    total2=0#其他项目重量
    processed=[]
    while 1:
        fneed=[]#存分配完的需求
        otherfneed=[]
        if templen==len(cproject):#无需求被满足，当前最短需求无法按长度组合分配
            #del cproject[0]#清除最短需求
            processed.append(item)#当前项目处理完毕
        else:
            templen=len(cproject)#长度更新

        #if len(cproject)==0:#每个需求都经过长度组合匹配
        if len(processed)==len(cproject):#项目不是处理过了就是满足了，结束
            break

        cproject.sort(key=lambda x:x.length)#需求按长度从小到大

        for i in range(len(cproject)):
            if cproject[i] not in processed:#取出最短的且没处理过的需求

                item=cproject[i]
                break

        for x in project:
            print(x.width,end=' ')
        print()

        print(item.width)
        times=int(cproject[-1].length/cproject[0].length)+1#最大倍数，最长需求/最短需求+1

        storage.sort(key=lambda x:(x.widthscale.right,str(x.id)),reverse=True)#母卷按长度从大到小

        max_roll_width=storage[0].widthscale.right#母卷最大宽度

        interval_now=[]#当前需求倍数范围
        relation=[]#与当前需求存在倍数关系的需求列表：（需求，倍数）
        scale=copy.deepcopy(item.lengthscale)#当前米数范围

        print(scale.left)
        print(scale.right)

        for num in range(1,times+1):#计算倍数范围
            interval_now.append(Interval(num*scale.left,num*scale.right))

        width_now=item.width#当前倍数组合宽度之和
            
        for need in sorted(cproject,key=lambda x:x.width,reverse=True):#找倍数关系，从最宽需求开始
            if need==item:#跳过自己
                continue
            c=1#倍数
            flag=0#是否找到满足倍数关系的需求
            for interval in interval_now:
                if isoverlap(interval,need.lengthscale):#范围有交集
                    flag=1
                    break
                c=c+1

            if flag==1 and width_now+need.width*c>max_roll_width:#有倍数关系，但宽度之和大于母卷最大宽度，舍弃
                flag=0

            if flag==1:#更新米数范围和倍数范围
                tempscale=copy.deepcopy(scale)
                temprolllist=[]

                scale=scale_update(scale,Interval(need.lengthscale.left/c,need.lengthscale.right/c))#更新米数范围

                for roll in storage:#寻找满足要求的母卷（长度正好落在需求米数范围内/长度比当前米数范围大的母卷）
                    if (inscale(roll.length,scale) or roll.length-scale.left>=min_length) and roll.widthscale.right>=width_now+need.width*c:
                        temprolllist.append(roll)
                if len(temprolllist)==0:#没有满足要求的母卷，下一个需求
                    scale=copy.deepcopy(tempscale)#恢复之前的米数范围
                else:#有满足要求的母卷
                    width_now=width_now+need.width*c
                    relation.append((need,c))
                    interval_now=[]
                    for num in range(1,times+1):#重新计算倍数范围
                        interval_now.append(Interval(num*scale.left,num*scale.right))

        for i in relation:
            print(i[0].width,i[1])

        print(scale.left)
        print(scale.right)
                    
        if len(relation)!=0:#存在倍数组合
            rolllist=[]#存满足长度需求的母卷：（母卷，切割长度）
            #长度正好落在需求米数范围内的 or 长度大于米数范围左边界 的母卷；长度、宽度都符合要求
            for roll in storage:
                if inscale(roll.length,scale) and roll.widthscale.right>=width_now:
                    rolllist.append((roll,roll.length))
                    #print('1 '+str(roll.id)+' '+str(roll.length))
            for roll in storage:#长度比需求米数范围大的母卷
                if roll.length-scale.left>=min_length and roll.widthscale.right>=width_now:#长度宽度满足基本要求
                    if inscale(item.length,scale) and roll_satisfy(roll.length,item.length,min_length):
                        rolllist.append((roll,item.length))
                        #print('2 '+str(roll.id)+' '+str(item.length))
                    else:
                        for i in range(int(scale.left),int(scale.right)+1):
                            if roll_satisfy(roll.length,i,min_length):
                                rolllist.append((roll,i))
                                #print('2 '+str(roll.id))
                                break
            if len(rolllist)==0:#没有满足要求的母卷，下一个需求
                continue

            rolllist.sort(key=lambda x:(x[0].widthscale.right,x[0].length,x[0].id),reverse=True)

            #优先用开过的母卷
            storagelist=[]

            for roll in rolllist:
                for b in range(0,rollindex):
                    if roll[0].id==idlist[b]:
                        storagelist.append(roll)
                        break

            for roll in rolllist:
                if roll not in storagelist:
                    storagelist.append(roll)
            
            rolllist=storagelist

            maxroll=rolllist[0]
            maxsum=width_now
            maxlist=relation
            content={}
            content['width']=[item.width,]
            content['symbol']=[sym['项目'][0],]
            for one in maxlist:
                for j in range(0,one[1]):
                    content['width'].append(one[0].width)
                    content['symbol'].append(sym['项目'][0])
            content['length']=maxroll[1]#方案长度
            
            if maxsum!=0:#有最优宽度组合
                
                for i in maxlist:#所有倍数需求完成
                    for j in project:
                        if i[0].width==j.width:
                            fneed.append(j)#组合内的需求完成
                            break
                for i in project:#当前需求完成
                    if i.width==item.width:
                        fneed.append(i)
                        break

                tempproject=[x for x in project if x not in fneed]#剩余需求
                
                new_widthscale=Interval(maxroll[0].widthscale.left-width_now,maxroll[0].widthscale.right-width_now)#剩余宽度
                if new_widthscale.left<0:
                    new_widthscale.left=0
        
                itemlist=[]#存满足长度宽度要求的剩余需求
                for one in tempproject:
                    if one.width<=new_widthscale.right and need_satisfy(one.length,maxroll[1],one.left,one.right,min_length):#满足长度宽度要求的剩余需求
                        itemlist.append(one)
                
                itemlist.sort(key=lambda x:x.width,reverse=True)#所有需求按宽度逆序排序

                maxnum=0#求组合内需求个数最大值
                if method==0:
                    tempsum=0
                    c=0
                    for p in range(len(itemlist)):
                        if tempsum>=new_widthscale.right:
                            break
                        tempsum=tempsum+itemlist[p].width
                        c=c+1
                    if tempsum!=0 and tempsum<new_widthscale.right:
                        maxnum=int(new_widthscale.right/tempsum+0.5)*c
                    else:
                        maxnum=c
                elif method==1:#平均数——母卷宽度范围右边界/需求宽度平均数
                    tempsum=0
                    c=0
                    for obj in itemlist:
                        if obj.width<new_widthscale.right:
                            tempsum=tempsum+obj.width
                            c=c+1
                    if c!=0:
                        avg=tempsum/c
                        maxnum=int(new_widthscale.right/avg)
                elif method==2:#中位数——母卷宽度范围右边界/需求宽度中位数
                    templist3=[]
                    for obj in itemlist:
                        if obj.width<=new_widthscale.right:
                            templist3.append(obj)
                    if len(templist3)!=0:
                        tempmark=int(len(templist3)/2)
                        if len(templist3)%2==0:
                            mid=(templist3[tempmark-1].width+templist3[tempmark].width)/2
                        else:
                            mid=templist3[tempmark].width
                        maxnum=int(new_widthscale.right/mid)
                elif method==3:#平均数+1
                    tempsum=0
                    c=0
                    for obj in itemlist:
                        if obj.width<new_widthscale.right:
                            tempsum=tempsum+obj.width
                            c=c+1
                    if c!=0:
                        avg=tempsum/c
                        maxnum=int(new_widthscale.right/avg)+1
                elif method==4:#平均数-1
                    tempsum=0
                    c=0
                    for obj in itemlist:
                        if obj.width<new_widthscale.right:
                            tempsum=tempsum+obj.width
                            c=c+1
                    if c!=0:
                        avg=tempsum/c
                        maxnum=int(new_widthscale.right/avg)-1
                elif method==5:#中位数+1
                    templist3=[]
                    for obj in itemlist:
                        if obj.width<=new_widthscale.right:
                            templist3.append(obj)
                    if len(templist3)!=0:
                        tempmark=int(len(templist3)/2)
                        if len(templist3)%2==0:
                            mid=(templist3[tempmark-1].width+templist3[tempmark].width)/2
                        else:
                            mid=templist3[tempmark].width
                        maxnum=int(new_widthscale.right/mid)+1
                elif method==6:#中位数-1
                    templist3=[]
                    for obj in itemlist:
                        if obj.width<=new_widthscale.right:
                            templist3.append(obj)
                    if len(templist3)!=0:
                        tempmark=int(len(templist3)/2)
                        if len(templist3)%2==0:
                            mid=(templist3[tempmark-1].width+templist3[tempmark].width)/2
                        else:
                            mid=templist3[tempmark].width
                        maxnum=int(new_widthscale.right/mid)-1
              
                i=1
                maxsum2=0
                maxlist2=[]
                minsum2=float('inf')
                while 1:#完成剩余宽度的组合分配
                    for subset in combinations_with_replacement(itemlist,i):#宽度所有组合
                        tempdic={}#存需求在组合中出现的次数
                        templist=[]#存不重复的需求

                        for one in subset:#初始化tempdic和templist
                            if one not in templist:
                                templist.append(one)
                                tempdic[str(one.width)]=0

                        for one in subset:#计算需求在组合中出现的次数
                            tempdic[str(one.width)]=tempdic[str(one.width)]+1
                        
                        flag=1#组合中需求是否都满足长度要求

                        for one in templist:
                            if need_satisfy(one.length,tempdic[str(one.width)]*maxroll[1],one.left,one.right,min_length)==False:
                                flag=0
                                break

                        tempsum=sum([x.width for x in subset])#计算宽度之和
                        if flag==1:
                            if tempsum>maxsum2 and tempsum<new_widthscale.right:#利用率更大
                                maxsum2=tempsum
                                maxlist2=list(subset)
                        if tempsum<minsum2:
                            minsum2=tempsum
                    if minsum2>=new_widthscale.right or i >= maxnum:
                        break
                    else:
                        minsum2=float('inf')
                        i=i+1

                print(item.width,end=' ')
                for x in maxlist:
                    print(x[0].width,end=' ')
                print(' and ',end='')
                for x in maxlist2:
                    print(x.width,end=' ')
                print()

                if maxsum2!=0:#存在最优宽度组合
                    for one in maxlist2:
                        content['width'].append(one.width)#存方案宽度
                        content['symbol'].append(sym['项目'][0])
                        for obj in project:#更新需求
                            if obj==one:
                                if obj.length-maxroll[1]<min_length:
                                    fneed.append(obj)
                                else:
                                    obj.length=obj.length-maxroll[1]
                                    obj.lengthscale.left=obj.length+obj.left
                                    obj.lengthscale.right=obj.length+obj.right

                        for sub in cproject:
                            if sub.width==one.width:
                                if sub.length-maxroll[1]>=min_length:
                                    sub.length=sub.length-maxroll[1]
                                    sub.lengthscale.left=sub.length+sub.left
                                    sub.lengthscale.right=sub.length+sub.right
          
                for width in content['width']:
                    total=total+cal_weight(width,content['length'],para)#计算主需求重量
                    prolist[0][str(width)].append((maxroll[0].id,content['length']))#主需求分配情况

                for index in range(len(otherproject)):#其他需求

                    tempproject=[x for x in otherproject[index] if x not in fneed]
                    print("剩余宽度："+str(maxroll[0].widthscale.right-maxsum2-width_now))
                    maxsum3,maxlist3=get_combination([],tempproject,content['length'],maxroll[0].widthscale.right-maxsum2-width_now,min_length,method)
                    maxsum2=maxsum2+maxsum3

                    for x in maxlist3:#更新方案
                        content['width'].append(x.width)
                        content['symbol'].append(sym['项目'][index+1])
                        
                    for need in maxlist3:

                        total2=total2+cal_weight(need.width,content['length'],para)#计算重量

                        if need.length-content['length']<min_length:#更新需求
                            otherfneed.append(need)
                        else:
                            need.length=need.length-content['length']
                            need.lengthscale.left=need.length+need.left
                            need.lengthscale.right=need.length+need.right

                        prolist[index+1][str(need.width)].append((maxroll[0].id,content['length']))#需求分配情况
 
                
                remainlist=remain_process(maxroll[0].widthscale.right-maxsum2-width_now,remain_min)#分配余材
                for width in remainlist:
                    content['width'].append(width)
                    content['symbol'].append(sym['余材'])

                width_sort(content['width'],content['symbol'])
                
                plan[maxroll[0].id].append(content)#存方案

                #记录
                temprecord={}
                temprecord['roll']=maxroll[0]
                temprecord['content']=content
                record[step].append(temprecord)

                for a in range(rollindex,len(idlist)):#更新母卷顺序
                    if idlist[a]==maxroll[0].id:
                        temp=idlist[a]
                        idlist[a]=idlist[rollindex]
                        idlist[rollindex]=temp
                        rollindex=rollindex+1
                        break

                print(maxroll[0].id)#母卷号

                print(content)

                for pro in cproject:
                    print(pro.width,end=' ')
                    print(pro.length,end=' ')
                    print(pro.lengthscale.left,end=' ')
                    print(pro.lengthscale.right)

                if maxroll[0].length-maxroll[1]<min_length:#更新母卷
                    storage.remove(maxroll[0])
                else:
                    for roll in storage:
                        if roll==maxroll[0]:
                            roll.length=roll.length-maxroll[1]
                            break

        project=[x for x in project if x not in fneed]#更新主需求
        for tempproject in otherproject:#更新其他需求
            tempproject=[x for x in tempproject if x not in otherfneed]

        for i in fneed:#主项目副本更新，去掉满足了的需求
            for j in cproject:
                if i.width==j.width:
                    cproject.remove(j)
                    break

    data={
        'project':project,
        'storage':storage,
        'plan':plan,
    }
    return data,total,total2,rollindex

def get_combination(lastwidth,project,cut_length,max_width,min_length,method):#已知切割长度和剩余宽度，获取最优宽度组合
    project.sort(key=lambda x:x.width,reverse=True)
    i=1
    maxsum=0
    maxlist=[]
    if len(project)==0:
        return maxsum,maxlist

    maxnum=0
    if method==0:
        tempsum=0
        c=0
        project.sort(key=lambda x:x.width)
        for p in range(len(project)):
            if tempsum>=max_width:
                break
            tempsum=tempsum+project[p].width
            c=c+1
        if tempsum!=0 and tempsum<max_width:
            maxnum=int(max_width/tempsum+0.5)*c
        else:
            maxnum=c
    elif method==1:#平均数——母卷宽度范围右边界/需求宽度平均数
        tempsum=0
        c=0
        for obj in project:
            if obj.width<max_width:
                tempsum=tempsum+obj.width
                c=c+1
        if c!=0:
            avg=tempsum/c
            maxnum=int(max_width/avg)
    elif method==2:#中位数——母卷宽度范围右边界/需求宽度中位数
        templist3=[]
        for obj in project:
            if obj.width<=max_width:
                templist3.append(obj)
        if len(templist3)!=0:
            tempmark=int(len(templist3)/2)
            if len(templist3)%2==0:
                mid=(templist3[tempmark-1].width+templist3[tempmark].width)/2
            else:
                mid=templist3[tempmark].width
            maxnum=int(max_width/mid)
    elif method==3:#平均数+1
        tempsum=0
        c=0
        for obj in project:
            if obj.width<max_width:
                tempsum=tempsum+obj.width
                c=c+1
        if c!=0:
            avg=tempsum/c
            maxnum=int(max_width/avg)+1
    elif method==4:#平均数-1
        tempsum=0
        c=0
        for obj in project:
            if obj.width<max_width:
                tempsum=tempsum+obj.width
                c=c+1
        if c!=0:
            avg=tempsum/c
            maxnum=int(max_width/avg)-1
    elif method==5:#中位数+1
        templist3=[]
        for obj in project:
            if obj.width<=max_width:
                templist3.append(obj)
        if len(templist3)!=0:
            tempmark=int(len(templist3)/2)
            if len(templist3)%2==0:
                mid=(templist3[tempmark-1].width+templist3[tempmark].width)/2
            else:
                mid=templist3[tempmark].width
            maxnum=int(max_width/mid)+1
    elif method==6:#中位数-1
        templist3=[]
        for obj in project:
            if obj.width<=max_width:
                templist3.append(obj)
        if len(templist3)!=0:
            tempmark=int(len(templist3)/2)
            if len(templist3)%2==0:
                mid=(templist3[tempmark-1].width+templist3[tempmark].width)/2
            else:
                mid=templist3[tempmark].width
            maxnum=int(max_width/mid)-1

    maxsim=0
    marksum=0

    while 1:
        minsum=float('inf')
        for subset in combinations_with_replacement(project,i):
            tempsum=sum([x.width for x in subset])
            if tempsum<=max_width and tempsum>maxsum:
                tempdic={}
                templist=[]

                for one in subset:
                    if one not in templist:
                        templist.append(one)
                        tempdic[str(one.width)]=0

                for one in subset:
                    tempdic[str(one.width)]=tempdic[str(one.width)]+1
                        
                flag=1

                for one in templist:
                    if need_satisfy(one.length,tempdic[str(one.width)]*cut_length,one.left,one.right,min_length)==False:
                        flag=0
                        break

                if flag==1:
                    maxsum=tempsum
                    maxlist=list(subset)
                    maxsim=0
            """ elif tempsum==maxsum:
                tempsim=0
                templist=[]
                for one in subset:#看和上一个宽度组合的相似度
                    templist.append(one.width)
                for tempwidth in lastwidth:
                    if tempwidth in templist:
                        tempsim=tempsim+1
                if tempsim>maxsim:
                    maxlist=list(subset)
                    maxsim=tempsim """
            if tempsum<minsum:
                minsum=tempsum

        if minsum>=max_width or i>=maxnum or marksum==maxsum:
            break
        else:
            i=i+1
            marksum=maxsum

    return maxsum,maxlist
   
def quick_match(need_not_done,need_same_width,lastwidth,roll,mainproject,otherproject,sym,prolist,para,fneed,min_length,method,allproject,remain_min,plan,froll,idlist,rollindex,record,step):

    #有需求被满足
    #母卷分配完且有需求被满足
    curwidth=0

    content={}
    content['width']=[]
    content['length']=roll.length#母卷全分配
    content['symbol']=[]
    total1=0
    total2=0

    tempproject=[x for x in mainproject if x not in fneed]#主需求

    for mainneed in tempproject:
        leftwidth=roll.widthscale.right-curwidth#剩余宽度
        maxnum=int(leftwidth/mainneed.width)#剩余宽度最多能容纳多少个当前需求

        for p in range(1,maxnum+1):#从1~maxnum个

            if inscale(content['length']*p,mainneed.lengthscale)==True:#需求恰好被满足

                for q in range(p):
                    content['width'].append(mainneed.width)
                    content['symbol'].append(sym['项目'][0])
                    curwidth=curwidth+mainneed.width
                    total1=total1+cal_weight(mainneed.width,content['length'],para)
                    prolist[0][str(mainneed.width)].append((roll.id,content['length']))
                
                fneed.append(mainneed)

                break

    if content['width']==[]:
        return [],{},0,0,rollindex

    alllist=[]

    need_not_done=[x for x in need_not_done if x not in fneed]

    maxsum0,maxlist0=get_maxlist0(need_not_done,need_same_width,fneed,content['length'],roll.widthscale.right-curwidth,min_length)

    alllist.extend(maxlist0)

    print("maxlist0:",end='')

    for x in maxlist0:
        print(x.width,end=' ')
    print()

    for x in maxlist0:

        if x in mainproject:
            content['width'].append(x.width)
            content['symbol'].append(sym['项目'][0])

            total1=total1+cal_weight(x.width,content['length'],para)

            prolist[0][str(x.width)].append((roll.id,content['length']))

        else:
            for index in range(len(otherproject)):

                if x in otherproject[index]:

                    content['width'].append(x.width)
                    content['symbol'].append(sym['项目'][index+1])

                    total2=total2+cal_weight(x.width,content['length'],para)

                    prolist[index+1][str(x.width)].append((roll.id,content['length']))

                    break
           
    tempproject=[x for x in mainproject if x not in fneed]#其他主需求
    maxsum,maxlist=get_combination(lastwidth,tempproject,content['length'],roll.widthscale.right-curwidth-maxsum0,min_length,method)
    
    alllist.extend(maxlist)

    for x in maxlist:#加入主需求
        content['width'].append(x.width)
        content['symbol'].append(sym['项目'][0])

        total1=total1+cal_weight(x.width,content['length'],para)

        if x.length-content['length']<min_length:
            fneed.append(x)
        else:
            x.length=x.length-content['length']
            x.lengthscale.left=x.length+x.left
            x.lengthscale.right=x.length+x.right

        prolist[0][str(x.width)].append((roll.id,content['length']))

    maxsum2=0#凑次需求

    for index in range(len(otherproject)):

        tempproject=[x for x in otherproject[index] if x not in fneed]
        maxsum3,maxlist=get_combination(lastwidth,tempproject,content['length'],roll.widthscale.right-curwidth-maxsum0-maxsum-maxsum2,min_length,method)
        maxsum2=maxsum2+maxsum3

        alllist.extend(maxlist)
            
        for x in maxlist:
            content['width'].append(x.width)
            content['symbol'].append(sym['项目'][index+1])

            total2=total2+cal_weight(x.width,content['length'],para)

            if x.length-content['length']<min_length:
                fneed.append(x)
            else:
                x.length=x.length-content['length']
                x.lengthscale.left=x.length+x.left
                x.lengthscale.right=x.length+x.right

            for c in range(1,len(allproject)):
                if x in allproject[c]:
                    prolist[c][str(x.width)].append((roll.id,content['length']))
                    break

    remainlist=remain_process(roll.widthscale.right-curwidth-maxsum0-maxsum-maxsum2,remain_min)#分配余材
    for width in remainlist:
        content['width'].append(width)
        content['symbol'].append(sym['余材'])

    froll.append(roll)

    plan[roll.id].append(content)

    #记录
    temprecord={}
    temprecord['roll']=roll
    temprecord['content']=content
    record[step].append(temprecord)

    for a in range(rollindex,len(idlist)):
        if idlist[a]==roll.id:
            temp=idlist[a]
            idlist[a]=idlist[rollindex]
            idlist[rollindex]=temp
            rollindex=rollindex+1
            break

    print(roll.id)

    width_sort(content['width'],content['symbol'])

    print(content)

    alllist=[x for x in alllist if x not in fneed]

    return alllist,content,total1,total2,rollindex

def quick_match_2(need_not_done,need_same_width,lastwidth,roll,mainproject,otherproject,sym,prolist,para,fneed,min_length,method,allproject,remain_min,plan,froll,idlist,rollindex,record,step):

    #母卷可以全部分配，不满足某个需求
    curwidth=0

    content={}
    content['width']=[]
    content['length']=roll.length
    content['symbol']=[]
    total1=0
    total2=0
    alllist=[]

    flag=0#是否有需求被剩下
           
    tempproject=[x for x in mainproject if x not in fneed]
    maxsum,maxlist=get_combination(lastwidth,tempproject,content['length'],roll.widthscale.right-curwidth,min_length,method)

    if maxsum==0:
        return [],-1,{},0,0,rollindex#没有任何主需求可以使母卷全部分配

    alllist.extend(maxlist)
    
    for x in maxlist:
        content['width'].append(x.width)
        content['symbol'].append(sym['项目'][0])

        total1=total1+cal_weight(x.width,content['length'],para)

        if x.length-content['length']<min_length:
            fneed.append(x)
            flag=1
        else:
            x.length=x.length-content['length']
            x.lengthscale.left=x.length+x.left
            x.lengthscale.right=x.length+x.right

        prolist[0][str(x.width)].append((roll.id,content['length']))

    need_not_done=[x for x in need_not_done if x not in fneed]

    templen=len(fneed)

    maxsum0,maxlist0=get_maxlist0(need_not_done,need_same_width,fneed,content['length'],roll.widthscale.right-curwidth-maxsum,min_length)

    alllist.extend(maxlist0)

    print("maxlist0:",end='')

    for x in maxlist0:
        print(x.width,end=' ')
    print()

    if templen!=len(fneed):
        flag=1

    for x in maxlist0:

        if x in mainproject:
            content['width'].append(x.width)
            content['symbol'].append(sym['项目'][0])

            total1=total1+cal_weight(x.width,content['length'],para)

            prolist[0][str(x.width)].append((roll.id,content['length']))

        else:
            for index in range(len(otherproject)):

                if x in otherproject[index]:

                    content['width'].append(x.width)
                    content['symbol'].append(sym['项目'][index+1])

                    total2=total2+cal_weight(x.width,content['length'],para)

                    prolist[index+1][str(x.width)].append((roll.id,content['length']))

                    break

    maxsum2=0

    for index in range(len(otherproject)):

        tempproject=[x for x in otherproject[index] if x not in fneed]
        maxsum3,maxlist=get_combination(lastwidth,tempproject,content['length'],roll.widthscale.right-curwidth-maxsum0-maxsum-maxsum2,min_length,method)
        maxsum2=maxsum2+maxsum3

        alllist.extend(maxlist)
            
        for x in maxlist:
            content['width'].append(x.width)
            content['symbol'].append(sym['项目'][index+1])

            total2=total2+cal_weight(x.width,content['length'],para)

            if x.length-content['length']<min_length:
                fneed.append(x)
                flag=1
            else:
                x.length=x.length-content['length']
                x.lengthscale.left=x.length+x.left
                x.lengthscale.right=x.length+x.right

            for c in range(1,len(allproject)):
                if x in allproject[c]:
                    prolist[c][str(x.width)].append((roll.id,content['length']))
                    break

    remainlist=remain_process(roll.widthscale.right-curwidth-maxsum0-maxsum-maxsum2,remain_min)
    for width in remainlist:
        content['width'].append(width)
        content['symbol'].append(sym['余材'])

    froll.append(roll)

    plan[roll.id].append(content)

    #记录
    temprecord={}
    temprecord['roll']=roll
    temprecord['content']=content
    record[step].append(temprecord)

    for a in range(rollindex,len(idlist)):
        if idlist[a]==roll.id:
            temp=idlist[a]
            idlist[a]=idlist[rollindex]
            idlist[rollindex]=temp
            rollindex=rollindex+1
            break

    print(roll.id)

    width_sort(content['width'],content['symbol'])

    print(content)

    alllist=[x for x in alllist if x not in fneed]

    return alllist,flag,content,total1,total2,rollindex

def quick_match_3(need_not_done,need_same_width,lastwidth,roll,mainproject,otherproject,sym,prolist,para,fneed,min_length,method,allproject,remain_min,plan,froll,idlist,rollindex,record,step):

    #母卷可以满足其他需求，优先满足其他需求
    curwidth=0

    content={}
    content['width']=[]
    content['symbol']=[]
    total1=0
    total2=0
    alllist=[]
           
    tempproject=[x for x in mainproject if x not in fneed]

    tempproject.sort(key=lambda x:x.width,reverse=True)

    for mainneed in tempproject:
        maxnum=int(roll.widthscale.right/mainneed.width)#剩余宽度最多能容纳多少个当前需求

        for p in range(1,maxnum+1):#从1~maxnum个

            if roll_satisfy(roll.length,mainneed.length/p,min_length)==True:#需求恰好被满足

                content['length']=mainneed.length/p

                for q in range(p):
                    content['width'].append(mainneed.width)
                    content['symbol'].append(sym['项目'][0])
                    curwidth=curwidth+mainneed.width
                    total1=total1+cal_weight(mainneed.width,content['length'],para)
                    prolist[0][str(mainneed.width)].append((roll.id,content['length']))
                
                fneed.append(mainneed)

                if roll.length-content['length']>=min_length:
                    roll.length=roll.length-content['length']
                else:
                    froll.append(roll)

                break
        
        if mainneed in fneed:
            break

    if content['width']==[]:
        return [],{},0,0,rollindex

    need_not_done=[x for x in need_not_done if x not in fneed]

    maxsum0,maxlist0=get_maxlist0(need_not_done,need_same_width,fneed,content['length'],roll.widthscale.right-curwidth,min_length)

    alllist.extend(maxlist0)

    print("maxlist0:",end='')

    for x in maxlist0:
        print(x.width,end=' ')
    print()

    for x in maxlist0:

        if x in mainproject:
            content['width'].append(x.width)
            content['symbol'].append(sym['项目'][0])

            total1=total1+cal_weight(x.width,content['length'],para)

            prolist[0][str(x.width)].append((roll.id,content['length']))

        else:
            for index in range(len(otherproject)):

                if x in otherproject[index]:

                    content['width'].append(x.width)
                    content['symbol'].append(sym['项目'][index+1])

                    total2=total2+cal_weight(x.width,content['length'],para)

                    prolist[index+1][str(x.width)].append((roll.id,content['length']))

                    break

    tempproject=[x for x in mainproject if x not in fneed]

    maxsum,maxlist=get_combination(lastwidth,tempproject,content['length'],roll.widthscale.right-curwidth-maxsum0,min_length,method)

    alllist.extend(maxlist)
    
    for x in maxlist:
        content['width'].append(x.width)
        content['symbol'].append(sym['项目'][0])

        total1=total1+cal_weight(x.width,content['length'],para)

        if x.length-content['length']<min_length:
            fneed.append(x)
        else:
            x.length=x.length-content['length']
            x.lengthscale.left=x.length+x.left
            x.lengthscale.right=x.length+x.right

        prolist[0][str(x.width)].append((roll.id,content['length']))

    maxsum2=0

    for index in range(len(otherproject)):


        tempproject=[x for x in otherproject[index] if x not in fneed]
        maxsum3,maxlist=get_combination(lastwidth,tempproject,content['length'],roll.widthscale.right-curwidth-maxsum0-maxsum-maxsum2,min_length,method)
        maxsum2=maxsum2+maxsum3

        alllist.extend(maxlist)
            
        for x in maxlist:
            content['width'].append(x.width)
            content['symbol'].append(sym['项目'][index+1])

            total2=total2+cal_weight(x.width,content['length'],para)

            if x.length-content['length']<min_length:
                fneed.append(x)
            else:
                x.length=x.length-content['length']
                x.lengthscale.left=x.length+x.left
                x.lengthscale.right=x.length+x.right

            for c in range(1,len(allproject)):
                if x in allproject[c]:
                    prolist[c][str(x.width)].append((roll.id,content['length']))
                    break

    remainlist=remain_process(roll.widthscale.right-curwidth-maxsum0-maxsum-maxsum2,remain_min)
    for width in remainlist:
        content['width'].append(width)
        content['symbol'].append(sym['余材'])

    plan[roll.id].append(content)

    #记录
    temprecord={}
    temprecord['roll']=roll
    temprecord['content']=content
    record[step].append(temprecord)

    for a in range(rollindex,len(idlist)):
        if idlist[a]==roll.id:
            temp=idlist[a]
            idlist[a]=idlist[rollindex]
            idlist[rollindex]=temp
            rollindex=rollindex+1
            break

    print(roll.id)

    width_sort(content['width'],content['symbol'])

    print(content)

    alllist=[x for x in alllist if x not in fneed]

    return alllist,content,total1,total2,rollindex

def cut(lastroll,roll,content_width,content_sym,sym,prolist,para,fneed,min_length,method,allproject,remain_min,plan,froll,idlist,rollindex,record,step):
   
    print("剩余组合分配：")
    tempsum=sum(content_width)

    mainneed=[]
    otherneed=[]
    allneed=[]
    total1=0
    total2=0

    for i in range(len(content_width)):#取出并区分宽度组合中的主需求、其他需求
        if content_sym[i] in sym['项目'][:-1]:
            project_id=sym['项目'].index(content_sym[i])
        else:
            continue
        
        for need in allproject[project_id]:
            if need.width==content_width[i]:
                if project_id==0:
                    mainneed.append(need)
                else:
                    otherneed.append(need)

    if roll.widthscale.right<tempsum or (roll.widthscale.left>tempsum and roll.widthscale.left-tempsum>=remain_min):#宽度指和不在母卷可用宽度范围内
        print("不在范围")
        return 0,0,0,rollindex,[]

    allneed.extend(mainneed)
    allneed.extend(otherneed)

    for x in mainneed:
        print(x.width,end=' ')
        print(x.length)

    tempdic2={}#存需求在组合中出现的次数
    templist2=[]#存不重复的需求

    for one in otherneed:#初始化tempdic和templist
        if one not in templist2:
            templist2.append(one)
            tempdic2[str(one.width)]=0

    for one in otherneed:#计算组合内需求出现的次数
        tempdic2[str(one.width)]=tempdic2[str(one.width)]+1

    tempdic={}#存需求在组合中出现的次数
    templist=[]#存不重复的需求

    tempdic2={}
    templist2=[]

    for one in mainneed:#初始化tempdic和templist
        if one not in templist:
            templist.append(one)
            tempdic[str(one.width)]=0

    for one in otherneed:#初始化tempdic和templist
        if one not in templist2:
            templist2.append(one)
            tempdic2[str(one.width)]=0

    for one in mainneed:#计算组合内需求出现的次数
        tempdic[str(one.width)]=tempdic[str(one.width)]+1

    for one in otherneed:#计算组合内需求出现的次数
        tempdic2[str(one.width)]=tempdic2[str(one.width)]+1

    shortneed=mainneed[0]#找出切割长度最短的主需求
    shortnum=tempdic[str(shortneed.width)]
    for tempitem in mainneed:
        if tempitem.length/tempdic[str(tempitem.width)]<shortneed.length/shortnum:
            shortneed=tempitem
            shortnum=tempdic[str(tempitem.width)]

    for tempitem in otherneed:
        if tempitem.length/tempdic2[str(tempitem.width)]<shortneed.length/shortnum:
            shortneed=tempitem
            shortnum=tempdic2[str(tempitem.width)]

    interval=copy.deepcopy(shortneed.lengthscale)#获取最短需求的米数范围
    num=shortnum

    if shortneed.length/num<min_length:#*************************************
        print("切割长度短")
        return 0,0,0,rollindex,[]

    tempflag=0
    cut_length=int(shortneed.length/num+0.5)

    interval.left=interval.left/num#更新米数范围
    interval.right=interval.right/num

    print("short_length:"+str(shortneed.length))

    isleft=0

    if need_satisfy(shortneed.length,roll.length*num,shortneed.left,shortneed.right,min_length):#母卷能全分配满足需求
        print('step 1:')
        tempflag=0
        for need in mainneed:
            if need_satisfy(need.length,roll.length*tempdic[str(need.width)],need.left,need.right,min_length)==False:
                tempflag=1
                break

        for need in otherneed:
            if need_satisfy(need.length,roll.length*tempdic2[str(need.width)],need.left,need.right,min_length)==False:
                tempflag=1
                break
        
        if tempflag==0:
            content={}
            content['width']=copy.deepcopy(content_width)
            content['length']=roll.length
            content['symbol']=copy.deepcopy(content_sym)

            tempflag2=0#是否有需求被满足

            for need in mainneed:

                total1=total1+cal_weight(need.width,content['length'],para)

                if need.length-content['length']<min_length:
                    fneed.append(need)
                    tempflag2=1
                else:
                    need.length=need.length-content['length']
                    need.lengthscale.left=need.length+need.left
                    need.lengthscale.right=need.length+need.right

                prolist[0][str(need.width)].append((roll.id,content['length']))

            for need in otherneed:
                total2=total2+cal_weight(need.width,content['length'],para)

                if need.length-content['length']<min_length:
                    fneed.append(need)
                    tempflag2=1
                else:
                    need.length=need.length-content['length']
                    need.lengthscale.left=need.length+need.left
                    need.lengthscale.right=need.length+need.right

                for i in range(len(allproject)):
                    if need in allproject[i]:
                        prolist[i][str(need.width)].append((roll.id,content['length']))
                        break

            froll.append(roll)

            plan[roll.id].insert(0,content)#连续组合置顶

            #记录
            temprecord={}
            temprecord['roll']=roll
            temprecord['content']=content
            record[step].append(temprecord)

        
            for a in range(rollindex,len(idlist)):
                if idlist[a]==roll.id:
                    temp=idlist[a]
                    idlist[a]=idlist[rollindex]
                    idlist[rollindex]=temp
                    rollindex=rollindex+1
                    break

            idlist.remove(roll.id)#放到上一卷母卷的后面
            idx=idlist.index(lastroll)
            idlist.insert(idx+1,roll.id)

            print(roll.id)

            width_sort(content['width'],content['symbol'])

            print(content)

            if tempflag2==0:
                print("没分配完")

                isleft=1

            
            return isleft,total1,total2,rollindex,content['width']

    
    if roll_satisfy(roll.length,cut_length,min_length):#母卷能满足需求
        print('step 2:')
        tempflag=0

        for need in mainneed:
            if need==shortneed:
                continue
            if need_satisfy(need.length,cut_length*tempdic[str(need.width)],need.left,need.right,min_length)==False:
                print(need.length,need.lengthscale.left,need.lengthscale.right)
                tempflag=1
                break

        for need in otherneed:
            if need_satisfy(need.length,cut_length*tempdic2[str(need.width)],need.left,need.right,min_length)==False:
                print(need.length,need.lengthscale.left,need.lengthscale.right)
                tempflag=1
                break
        
        if tempflag==0:
            content={}
            content['width']=copy.deepcopy(content_width)
            content['length']=cut_length
            content['symbol']=copy.deepcopy(content_sym)

            for need in mainneed:

                total1=total1+cal_weight(need.width,content['length'],para)

                if need.length-content['length']<min_length:
                    fneed.append(need)
                else:
                    need.length=need.length-content['length']
                    need.lengthscale.left=need.length+need.left
                    need.lengthscale.right=need.length+need.right

                prolist[0][str(need.width)].append((roll.id,content['length']))

            for need in otherneed:
                total2=total2+cal_weight(need.width,content['length'],para)

                if need.length-content['length']<min_length:
                    fneed.append(need)
                else:
                    need.length=need.length-content['length']
                    need.lengthscale.left=need.length+need.left
                    need.lengthscale.right=need.length+need.right

                for i in range(len(allproject)):
                    if need in allproject[i]:
                        prolist[i][str(need.width)].append((roll.id,content['length']))
                        break
            
            if roll.length-content['length']<min_length:
                froll.append(roll)
            else:
                roll.length=roll.length-content['length']

            plan[roll.id].insert(0,content)#连续组合指定

            #记录
            temprecord={}
            temprecord['roll']=roll
            temprecord['content']=content
            record[step].append(temprecord)

            for a in range(rollindex,len(idlist)):
                if idlist[a]==roll.id:
                    temp=idlist[a]
                    idlist[a]=idlist[rollindex]
                    idlist[rollindex]=temp
                    rollindex=rollindex+1
                    break

            idlist.remove(roll.id)#放到上一卷母卷后面
            idx=idlist.index(lastroll)
            idlist.insert(idx+1,roll.id)

            print(roll.id)
            
            width_sort(content['width'],content['symbol'])

            print(content)
            
            return isleft,total1,total2,rollindex,content['width']

    for i in range(int(max(interval.left,min_length)),int(interval.right)+1):#母卷能满足需求
        if roll_satisfy(roll.length,i,min_length)==True:


            tempflag=0

            for need in mainneed:
                if need_satisfy(need.length,i*tempdic[str(need.width)],need.left,need.right,min_length)==False:
                    tempflag=1
                    break

            for need in otherneed:
                if need_satisfy(need.length,i*tempdic2[str(need.width)],need.left,need.right,min_length)==False:
                    tempflag=1
                    break
                    
            if tempflag==0:

                print('step 3:')

                content={}
                content['width']=copy.deepcopy(content_width)
                content['length']=i
                content['symbol']=copy.deepcopy(content_sym)

                for need in mainneed:

                    total1=total1+cal_weight(need.width,content['length'],para)

                    if need.length-content['length']<min_length:
                        fneed.append(need)
                    else:
                        need.length=need.length-content['length']
                        need.lengthscale.left=need.length+need.left
                        need.lengthscale.right=need.length+need.right

                    prolist[0][str(need.width)].append((roll.id,content['length']))

                for need in otherneed:
                    total2=total2+cal_weight(need.width,content['length'],para)

                    if need.length-content['length']<min_length:
                        fneed.append(need)
                    else:
                        need.length=need.length-content['length']
                        need.lengthscale.left=need.length+need.left
                        need.lengthscale.right=need.length+need.right

                    for i in range(len(allproject)):
                        if need in allproject[i]:
                            prolist[i][str(need.width)].append((roll.id,content['length']))
                            break
                
                if roll.length-content['length']<min_length:
                    froll.append(roll)
                else:
                    roll.length=roll.length-content['length']

                plan[roll.id].insert(0,content)#连续组合置顶

                #记录
                temprecord={}
                temprecord['roll']=roll
                temprecord['content']=content
                record[step].append(temprecord)

                for a in range(rollindex,len(idlist)):
                    if idlist[a]==roll.id:
                        temp=idlist[a]
                        idlist[a]=idlist[rollindex]
                        idlist[rollindex]=temp
                        rollindex=rollindex+1
                        break

                idlist.remove(roll.id)#放在上一卷母卷后面
                idx=idlist.index(lastroll)
                idlist.insert(idx+1,roll.id)

                print(roll.id)

                width_sort(content['width'],content['symbol'])

                print(content)
                
                return isleft,total1,total2,rollindex,content['width']
        
    print("切不了")
    return isleft,0,0,rollindex,[]

def get_maxlist0(needs,sameneeds,fneed,cut_length,max_width,min_length):

    needs.sort(key=lambda x:x.width,reverse=True)

    maxlist=[]
    maxsum=0
    curwidth=0

    for need in needs:
        if need.width+curwidth<=max_width:
            if need_satisfy(need.length,cut_length,need.left,need.right,min_length):
                maxsum=maxsum+need.width
                maxlist.append(need)
                curwidth=curwidth+need.width
                if need.length-cut_length<min_length:
                    fneed.append(need)
                else:
                    need.length=need.length-cut_length
                    need.lengthscale.left=need.length+need.left
                    need.lengthscale.right=need.length+need.right
            else:
                for x in sameneeds:
                    if x.width==need.width and need_satisfy(x.length,cut_length,x.left,x.right,min_length):
                        maxsum=maxsum+x.width
                        maxlist.append(x)
                        curwidth=curwidth+x.width
                        if x.length-cut_length<min_length:
                            fneed.append(x)
                        else:
                            x.length=x.length-cut_length
                            x.lengthscale.left=x.length+x.left
                            x.lengthscale.right=x.length+x.right

                        break
    return maxsum,maxlist

def width_sort(width,sym):
    for i in range(len(width)-1):
        for j in range(i+1,len(width)):
            if width[i]<width[j]:
                temp=width[i]
                width[i]=width[j]
                width[j]=temp

                temp=sym[i]
                sym[i]=sym[j]
                sym[j]=temp


def all_match(mainproject,otherproject,storage,prolist,allproject,para,min_length,plan,remain_min,sym,method,idlist,rollindex,sorted_storage,left_cut,record,step):#最后一步分配完所有主需求
    
    mainproject.sort(key=lambda x:x.length)#主项目按长度从小到大
    fneed=[]#存分配完的需求
    total1=0
    total2=0

    lastwidth=[]

    need_not_done=[]

    need_same_width=[]

    for mainneed in mainproject:#对于每一个主需求

        if mainneed in fneed:#需求已完成
            continue

        print(mainneed.width)

        storage.sort(key=lambda x:(x.widthscale.right,str(x.id)),reverse=True)#母卷按宽度从大到小

        for roll in storage:
            print(roll.id, end=' ')
        print()

        #用过的母卷排前面
        storagelist=[]

        for roll in storage:
            for b in range(0,rollindex):
                if roll.id==idlist[b]:
                    storagelist.append(roll)
                    break

        for roll in storage:
            if roll not in storagelist:
                storagelist.append(roll)
        
        storage=storagelist

        for roll in storage:
            print(roll.id, end=' ')
        print()

        froll=[]#存分配完的母卷
        content={}#存当前主需求的方案

        isleft=0#组合是否未完成
        leftneed=[]#未完成组合宽度
        leftsym=[]#未完成组合符号

        for roll in storage:#遍历所有母卷

            if mainneed in fneed:#需求已完成，退出
                break

            if roll.widthscale.right<mainneed.width:#母卷宽度不满足需求，换下一卷
                continue

            m=0
            n=1
            templen=roll.length

            while 1:
                if roll in froll or (templen==roll.length and m==1 and n==1):#母卷已用完 or 母卷未作任何分配（不是第一次也不是剩余组合分配），退出
                    break

                if templen==roll.length and m==0:#第一次
                    m=1

                if templen==roll.length and n==0:#剩余组合分配不成功
                    n=1
                
                if templen!=roll.length:#更新templen
                    templen=roll.length

                if mainneed in fneed:#需求已完成，退出
                    break

                for need in otherproject[1]:
                    if need.width==120:
                        print(need.width,end=' ')
                        print(need.lengthscale.left,end=' ')
                        print(need.lengthscale.right)

                    break

                content={}#初始化方案

                print(roll.id)
                for p in fneed:
                    print(p.width,end=' ')
                print()

                print("isleft:"+str(isleft))#是否有剩余组合

                if isleft==1 and roll.id not in sorted_storage:#有剩余组合，且当前母卷无连续关系
                    tempsum=sum(leftneed)#组合宽度之和
                    n=0#当前分配的是剩余组合

                    #宽度之和在母卷宽度范围内 or 不在范围内但相差不超过余材规格
                    if inscale(tempsum,roll.widthscale) or (roll.widthscale.left>tempsum and roll.widthscale.left-tempsum<remain_min):
                        isleft,d1,d2,rollindex,tempwidth=cut(lastroll,roll,leftneed,leftsym,sym,prolist,para,fneed,min_length,method,allproject,remain_min,plan,froll,idlist,rollindex,record,step)
                        total1=total1+d1
                        total2=total2+d2 
                        #注意：母卷要么分配完，要么满足需求组合

                        if d1!=0:#剩余组合被分配
                            left_cut=left_cut+1#连续配刀数+1
                            sorted_storage.append(roll.id)#当前母卷有连续关系
                            lastwidth=tempwidth
                            print("连续")

                        if isleft==1:#还没分配完
                            lastroll=roll.id#当前母卷作为上一卷
                            break

                    else:#剩余需求组合不能被分配
                        isleft=0
                    continue#当前母卷继续分配


                #母卷全分配 and 满足需求    
                templist,result,d1,d2,rollindex=quick_match(need_not_done,need_same_width,lastwidth,roll,mainproject,otherproject,sym,prolist,para,fneed,min_length,method,allproject,remain_min,plan,froll,idlist,rollindex,record,step)
                total1=total1+d1
                total2=total2+d2

                print(rollindex)

                if result!={}:#成功分配，换下一卷
                    print('quick 1')
                    lastwidth=result['width']
                    need_not_done=templist
                    break

                if need_satisfy(mainneed.length,roll.length,mainneed.left,mainneed.right,min_length)==True:#母卷全分配

                    tempflag=0

                    print('step 1:')

                    content['width']=[mainneed.width,]#先分配主需求
                    content['symbol']=[sym['项目'][0],]
                    content['length']=roll.length

                    if mainneed.length-content['length']<min_length:
                        fneed.append(mainneed)
                        tempflag=1
                    else:
                        mainneed.length=mainneed.length-content['length']
                        mainneed.lengthscale.left=mainneed.length+mainneed.left
                        mainneed.lengthscale.right=mainneed.length+mainneed.right

                    total1=total1+cal_weight(mainneed.width,content['length'],para)

                    prolist[0][str(mainneed.width)].append((roll.id,content['length']))

                    alllist=[]
                    if mainneed not in fneed:
                        alllist.append(mainneed)

                    need_not_done=[x for x in need_not_done if x not in fneed]

                    templen=len(fneed)

                    maxsum0,maxlist0=get_maxlist0(need_not_done,need_same_width,fneed,content['length'],roll.widthscale.right-mainneed.width,min_length)

                    alllist.extend(maxlist0)

                    print("maxlist0",end='')

                    for x in maxlist0:
                        print(x.width,end=' ')
                    print()

                    if templen!=len(fneed):
                        tempflag=1

                    for x in maxlist0:

                        if x in mainproject:
                            content['width'].append(x.width)
                            content['symbol'].append(sym['项目'][0])

                            total1=total1+cal_weight(x.width,content['length'],para)

                            prolist[0][str(x.width)].append((roll.id,content['length']))

                        else:
                            for index in range(len(otherproject)):

                                if x in otherproject[index]:

                                    content['width'].append(x.width)
                                    content['symbol'].append(sym['项目'][index+1])

                                    total2=total2+cal_weight(x.width,content['length'],para)

                                    prolist[index+1][str(x.width)].append((roll.id,content['length']))

                                    break

                    tempproject=[x for x in mainproject if x not in fneed]
                    maxsum,maxlist=get_combination(lastwidth,tempproject,roll.length,roll.widthscale.right-mainneed.width-maxsum0,min_length,method)
                    
                    alllist.extend(maxlist)

                    for x in maxlist:
                        content['width'].append(x.width)
                        content['symbol'].append(sym['项目'][0])

                        total1=total1+cal_weight(x.width,content['length'],para)

                        if x.length-content['length']<min_length:
                            fneed.append(x)
                            tempflag=1
                        else:
                            x.length=x.length-content['length']
                            x.lengthscale.left=x.length+x.left
                            x.lengthscale.right=x.length+x.right

                        prolist[0][str(x.width)].append((roll.id,content['length']))

                    maxsum2=0

                    for index in range(len(otherproject)):


                        tempproject=[x for x in otherproject[index] if x not in fneed]
                        maxsum3,maxlist=get_combination(lastwidth,tempproject,content['length'],roll.widthscale.right-mainneed.width-maxsum0-maxsum-maxsum2,min_length,method)
                        maxsum2=maxsum2+maxsum3

                        alllist.extend(maxlist)
                        
                        for x in maxlist:
                            content['width'].append(x.width)
                            content['symbol'].append(sym['项目'][index+1])

                            total2=total2+cal_weight(x.width,content['length'],para)

                            if x.length-content['length']<min_length:
                                fneed.append(x)
                                tempflag=1
                            else:
                                x.length=x.length-content['length']
                                x.lengthscale.left=x.length+x.left
                                x.lengthscale.right=x.length+x.right

                            for c in range(1,len(allproject)):
                                if x in allproject[c]:
                                    prolist[c][str(x.width)].append((roll.id,content['length']))
                                    break

                    remainlist=remain_process(roll.widthscale.right-mainneed.width-maxsum0-maxsum-maxsum2,remain_min)
                    for width in remainlist:
                        content['width'].append(width)
                        content['symbol'].append(sym['余材'])
                    #content['width'].extend(remain_process(roll.widthscale.right-mainneed.width-maxsum-maxsum2,sidebar,remain_min))#分配边条/余材
                    froll.append(roll)

                    width_sort(content['width'],content['symbol'])

                    plan[roll.id].append(content)

                    #记录
                    temprecord={}
                    temprecord['roll']=roll
                    temprecord['content']=content
                    record[step].append(temprecord)

                    for a in range(rollindex,len(idlist)):
                        if idlist[a]==roll.id:
                            temp=idlist[a]
                            idlist[a]=idlist[rollindex]
                            idlist[rollindex]=temp
                            rollindex=rollindex+1
                            break

                    if tempflag==0:
                        print("剩下")

                        isleft=1
                        leftneed=copy.deepcopy(content['width'])
                        leftsym=copy.deepcopy(content['symbol'])
                        lastroll=roll.id


                    print(roll.id)

                    print(content)

                    lastwidth=content['width']

                    need_not_done=[x for x in alllist if x not in fneed]

                    need_same_width=[]

                    for x in alllist:
                        for tempneed in mainproject:
                            if tempneed.width==x.width:
                                if tempneed not in alllist and tempneed not in fneed:
                                    need_same_width.append(tempneed)
                                break
                        for index in range(len(otherproject)):
                            for tempneed in otherproject[index]:
                                if tempneed.width==x.width:
                                    if tempneed not in alllist and tempneed not in fneed:
                                        need_same_width.append(tempneed)
                                    break


                    break #退出

                if roll_satisfy(roll.length,mainneed.length,min_length)==True:#母卷可以恰好满足需求，需求完成，母卷可能有剩余

                    print('step 2:')

                    content['width']=[mainneed.width,]
                    content['length']=mainneed.length
                    content['symbol']=[sym['项目'][0],]
                    fneed.append(mainneed)

                    total1=total1+cal_weight(mainneed.width,content['length'],para)

                    prolist[0][str(mainneed.width)].append((roll.id,content['length']))

                    alllist=[]

                    need_not_done=[x for x in need_not_done if x not in fneed]

                    print("need_not_done:")
                    for x in need_not_done:
                        print(x.width,end=' ')
                    print()

                    maxsum0,maxlist0=get_maxlist0(need_not_done,need_same_width,fneed,content['length'],roll.widthscale.right-mainneed.width,min_length)

                    alllist.extend(maxlist0)

                    print("maxlist0:",end='')

                    for x in maxlist0:
                        print(x.width,end=' ')
                    print()

                    for x in maxlist0:

                        if x in mainproject:
                            content['width'].append(x.width)
                            content['symbol'].append(sym['项目'][0])

                            total1=total1+cal_weight(x.width,content['length'],para)

                            prolist[0][str(x.width)].append((roll.id,content['length']))

                        else:
                            for index in range(len(otherproject)):

                                if x in otherproject[index]:

                                    content['width'].append(x.width)
                                    content['symbol'].append(sym['项目'][index+1])

                                    total2=total2+cal_weight(x.width,content['length'],para)

                                    prolist[index+1][str(x.width)].append((roll.id,content['length']))

                    tempproject=[x for x in mainproject if x not in fneed]
                    maxsum,maxlist=get_combination(lastwidth,tempproject,mainneed.length,roll.widthscale.right-mainneed.width-maxsum0,min_length,method)
                    
                    alllist.extend(maxlist)
                    
                    for x in maxlist:
                        content['width'].append(x.width)
                        content['symbol'].append(sym['项目'][0])

                        total1=total1+cal_weight(x.width,mainneed.length,para)

                        if x.length-mainneed.length<min_length:
                            fneed.append(x)
                        else:
                            x.length=x.length-content['length']
                            x.lengthscale.left=x.length+x.left
                            x.lengthscale.right=x.length+x.right

                        prolist[0][str(x.width)].append((roll.id,content['length']))

                    maxsum2=0

                    for index in range(len(otherproject)):

                        tempproject=[x for x in otherproject[index] if x not in fneed]
                        
                        maxsum3,maxlist=get_combination(lastwidth,tempproject,mainneed.length,roll.widthscale.right-mainneed.width-maxsum0-maxsum-maxsum2,min_length,method)
                        maxsum2=maxsum2+maxsum3

                        alllist.extend(maxlist)
                        
                        for x in maxlist:
                            content['width'].append(x.width)
                            content['symbol'].append(sym['项目'][index+1])

                            total2=total2+cal_weight(x.width,mainneed.length,para)

                            if x.length-mainneed.length<min_length:
                                fneed.append(x)
                            else:
                                x.length=x.length-content['length']
                                x.lengthscale.left=x.length+x.left
                                x.lengthscale.right=x.length+x.right

                            for c in range(1,len(allproject)):
                                if x in allproject[c]:
                                    prolist[c][str(x.width)].append((roll.id,content['length']))
                                    break


                    remainlist=remain_process(roll.widthscale.right-mainneed.width-maxsum0-maxsum-maxsum2,remain_min)
                    for width in remainlist:
                        content['width'].append(width)
                        content['symbol'].append(sym['余材'])
                    
                    if roll.length-content['length']<min_length:
                        froll.append(roll)
                    else:
                        roll.length=roll.length-content['length']

                    width_sort(content['width'],content['symbol'])

                    plan[roll.id].append(content)

                    #记录
                    temprecord={}
                    temprecord['roll']=roll
                    temprecord['content']=content
                    record[step].append(temprecord)

                    for a in range(rollindex,len(idlist)):
                        if idlist[a]==roll.id:
                            temp=idlist[a]
                            idlist[a]=idlist[rollindex]
                            idlist[rollindex]=temp
                            rollindex=rollindex+1
                            break

                    print(roll.id)

                    print(content)

                    lastwidth=content['width']

                    need_not_done=[x for x in alllist if x not in fneed]

                    need_same_width=[]

                    for x in alllist:
                        for tempneed in mainproject:
                            if tempneed.width==x.width:
                                if tempneed not in alllist and tempneed not in fneed:
                                    need_same_width.append(tempneed)
                                break
                        for index in range(len(otherproject)):
                            for tempneed in otherproject[index]:
                                if tempneed.width==x.width:
                                    if tempneed not in alllist and tempneed not in fneed:
                                        need_same_width.append(tempneed)
                                    break

                    break#需求完成，退出


                flag=0
                #for i in range(int(mainneed.lengthscale.left),int(mainneed.lengthscale.right)):
                for i in range(int(max(mainneed.lengthscale.left,min_length)),int(mainneed.lengthscale.right)+1):
                #for i in range(int(max(mainneed.lengthscale.left,min_length)),int(mainneed.lengthscale.right)):#满足需求溢短差，需求完成，母卷可能有剩余
                    if roll_satisfy(roll.length,i,min_length)==True:

                        print('step 3:')

                        content['width']=[mainneed.width,]
                        content['length']=i
                        content['symbol']=[sym['项目'][0],]
                        fneed.append(mainneed)

                        total1=total1+cal_weight(mainneed.width,content['length'],para)

                        prolist[0][str(mainneed.width)].append((roll.id,content['length']))

                        alllist=[]

                        need_not_done=[x for x in need_not_done if x not in fneed]

                        maxsum0,maxlist0=get_maxlist0(need_not_done,need_same_width,fneed,content['length'],roll.widthscale.right-mainneed.width,min_length)

                        alllist.extend(maxlist0)

                        print("maxlist0",end='')

                        for x in maxlist0:
                            print(x.width,end=' ')
                        print()

                        for x in maxlist0:

                            if x in mainproject:
                                content['width'].append(x.width)
                                content['symbol'].append(sym['项目'][0])

                                total1=total1+cal_weight(x.width,content['length'],para)

                                prolist[0][str(x.width)].append((roll.id,content['length']))

                            else:
                                for index in range(len(otherproject)):

                                    if x in otherproject[index]:

                                        content['width'].append(x.width)
                                        content['symbol'].append(sym['项目'][index+1])

                                        total2=total2+cal_weight(x.width,content['length'],para)

                                        prolist[index+1][str(x.width)].append((roll.id,content['length']))

                        tempproject=[x for x in mainproject if x not in fneed]
                        maxsum,maxlist=get_combination(lastwidth,tempproject,content['length'],roll.widthscale.right-mainneed.width-maxsum0,min_length,method)
                        
                        alllist.extend(maxlist)
                        
                        for x in maxlist:
                            content['width'].append(x.width)
                            content['symbol'].append(sym['项目'][0])

                            total1=total1+cal_weight(x.width,content['length'],para)

                            if x.length-content['length']<min_length:
                                fneed.append(x)
                            else:
                                x.length=x.length-content['length']
                                x.lengthscale.left=x.length+x.left
                                x.lengthscale.right=x.length+x.right

                            prolist[0][str(x.width)].append((roll.id,content['length']))

                        maxsum2=0

                        for index in range(len(otherproject)):

                            tempproject=[x for x in otherproject[index] if x not in fneed]
                            maxsum3,maxlist=get_combination(lastwidth,tempproject,content['length'],roll.widthscale.right-mainneed.width-maxsum0-maxsum-maxsum2,min_length,method)
                            maxsum2=maxsum2+maxsum3

                            alllist.extend(maxlist)

                            for x in maxlist:
                                content['width'].append(x.width)
                                content['symbol'].append(sym['项目'][index+1])

                                total2=total2+cal_weight(x.width,content['length'],para)

                                if x.length-content['length']<min_length:
                                    fneed.append(x)
                                else:
                                    x.length=x.length-content['length']
                                    x.lengthscale.left=x.length+x.left
                                    x.lengthscale.right=x.length+x.right

                                for c in range(1,len(allproject)):
                                    if x in allproject[c]:
                                        prolist[c][str(x.width)].append((roll.id,content['length']))
                                        break

                        remainlist=remain_process(roll.widthscale.right-mainneed.width-maxsum0-maxsum-maxsum2,remain_min)
                        for width in remainlist:
                            content['width'].append(width)
                            content['symbol'].append(sym['余材'])

                        if roll.length-content['length']<min_length:
                            froll.append(roll)
                        else:
                            roll.length=roll.length-content['length']

                        flag=1

                        width_sort(content['width'],content['symbol'])

                        plan[roll.id].append(content)

                        #记录
                        temprecord={}
                        temprecord['roll']=roll
                        temprecord['content']=content
                        record[step].append(temprecord)

                        for a in range(rollindex,len(idlist)):
                            if idlist[a]==roll.id:
                                temp=idlist[a]
                                idlist[a]=idlist[rollindex]
                                idlist[rollindex]=temp
                                rollindex=rollindex+1   
                                break

                        print(roll.id)

                        print(content)

                        lastwidth=content['width']

                        need_not_done=[x for x in alllist if x not in fneed]

                        need_same_width=[]

                        for x in alllist:
                            for tempneed in mainproject:
                                if tempneed.width==x.width:
                                    if tempneed not in alllist and tempneed not in fneed:
                                        need_same_width.append(tempneed)
                                    break
                            for index in range(len(otherproject)):
                                for tempneed in otherproject[index]:
                                    if tempneed.width==x.width:
                                        if tempneed not in alllist and tempneed not in fneed:
                                            need_same_width.append(tempneed)
                                        break

                        break

                if flag==1:
                    break#需求满足，退出

                #母卷全分配，需求不一定满足
                templist,tempflag,result2,d1,d2,rollindex=quick_match_2(need_not_done,need_same_width,lastwidth,roll,mainproject,otherproject,sym,prolist,para,fneed,min_length,method,allproject,remain_min,plan,froll,idlist,rollindex,record,step)
                #for i in range(int(mainneed.length-min_length),0,-1):
                total1=total1+d1
                total2=total2+d2

                if tempflag==0:#没分配完
                    isleft=1
                    leftneed=copy.deepcopy(result2['width'])
                    leftsym=copy.deepcopy(result2['symbol'])
                    lastroll=roll.id
                    print("没分配完 2")

                if result2!={}:#成功分配
                    print('quick2')
                    lastwidth=result2['width']
                    need_not_done=templist
                    break
            
                else:#分配其他需求，需求满足，母卷不一定分完
                    templist,result3,d1,d2,rollindex=quick_match_3(need_not_done,need_same_width,lastwidth,roll,mainproject,otherproject,sym,prolist,para,fneed,min_length,method,allproject,remain_min,plan,froll,idlist,rollindex,record,step)
                    total1=total1+d1
                    total2=total2+d2

                    if result3!={}:#成功分配
                        lastwidth=result3['width']
                        need_not_done=templist
                        print('quick3')
            
                    else:
                        for i in range(int(mainneed.length-min_length),min_length-1,-1):#满足需求最短米数

                            if roll_satisfy(roll.length,i,min_length):

                                print('step 4:')

                                content['width']=[mainneed.width,]
                                content['length']=i
                                content['symbol']=[sym['项目'][0],]

                                total1=total1+cal_weight(mainneed.width,content['length'],para)

                                mainneed.length=mainneed.length-content['length']
                                mainneed.lengthscale.left=mainneed.length+mainneed.left
                                mainneed.lengthscale.right=mainneed.length+mainneed.right

                                prolist[0][str(mainneed.width)].append((roll.id,content['length']))

                                alllist=[mainneed,]

                                need_not_done=[x for x in need_not_done if x not in fneed]

                                maxsum0,maxlist0=get_maxlist0(need_not_done,fneed,content['length'],roll.widthscale.right-mainneed.width,min_length)

                                alllist.extend(maxlist0)

                                print("maxlist0",end='')

                                for x in maxlist0:
                                    print(x.width,end=' ')
                                print()


                                for x in maxlist0:

                                    if x in mainproject:
                                        content['width'].append(x.width)
                                        content['symbol'].append(sym['项目'][0])

                                        total1=total1+cal_weight(x.width,content['length'],para)

                                        prolist[0][str(x.width)].append((roll.id,content['length']))

                                    else:
                                        for index in range(len(otherproject)):

                                            if x in otherproject[index]:

                                                content['width'].append(x.width)
                                                content['symbol'].append(sym['项目'][index+1])

                                                total2=total2+cal_weight(x.width,content['length'],para)

                                                prolist[index+1][str(x.width)].append((roll.id,content['length']))

                                tempproject=[x for x in mainproject if x not in fneed]
                                maxsum,maxlist=get_combination(lastwidth,tempproject,content['length'],roll.widthscale.right-mainneed.width-maxsum0,min_length,method)
                                
                                alllist.extend(maxlist)
                                
                                for x in maxlist:
                                    content['width'].append(x.width)
                                    content['symbol'].append(sym['项目'][0])

                                    total1=total1+cal_weight(x.width,content['length'],para)

                                    if x.length-content['length']<min_length:
                                        fneed.append(x)
                                    else:
                                        x.length=x.length-content['length']
                                        x.lengthscale.left=x.length+x.left
                                        x.lengthscale.right=x.length+x.right

                                    prolist[0][str(x.width)].append((roll.id,content['length']))

                                maxsum2=0

                                for index in range(len(otherproject)):

                                    tempproject=[x for x in otherproject[index] if x not in fneed]
                                    maxsum3,maxlist=get_combination(lastwidth,tempproject,content['length'],roll.widthscale.right-mainneed.width-maxsum0-maxsum-maxsum2,min_length,method)
                                    maxsum2=maxsum2+maxsum3

                                    alllist.extend(maxlist)

                                    for x in maxlist:
                                        content['width'].append(x.width)
                                        content['symbol'].append(sym['项目'][index+1])

                                        total2=total2+cal_weight(x.width,content['length'],para)

                                        if x.length-content['length']<min_length:
                                            fneed.append(x)
                                        else:
                                            x.length=x.length-content['length']
                                            x.lengthscale.left=x.length+x.left
                                            x.lengthscale.right=x.length+x.right

                                        for c in range(1,len(allproject)):
                                            if x in allproject[c]:
                                                prolist[c][str(x.width)].append((roll.id,content['length']))
                                                break

                                remainlist=remain_process(roll.widthscale.right-mainneed.width-maxsum0-maxsum-maxsum2,remain_min)
                                for width in remainlist:
                                    content['width'].append(width)
                                    content['symbol'].append(sym['余材'])

                                if roll.length-content['length']<min_length:
                                    froll.append(roll)
                                    isleft=1
                                    leftneed=copy.deepcopy(content['width'])
                                    leftsym=copy.deepcopy(content['symbol'])
                                    lastroll=roll.id
                                else:
                                    roll.length=roll.length-content['length']

                                width_sort(content['width'],content['symbol'])

                                plan[roll.id].append(content)

                                #记录
                                temprecord={}
                                temprecord['roll']=roll
                                temprecord['content']=content
                                record[step].append(temprecord)

                                for a in range(rollindex,len(idlist)):
                                    if idlist[a]==roll.id:
                                        temp=idlist[a]
                                        idlist[a]=idlist[rollindex]
                                        idlist[rollindex]=temp
                                        rollindex=rollindex+1
                                        break

                                print(roll.id)

                                print(content)

                                lastwidth=content['width']

                                need_not_done=[x for x in alllist if x not in fneed]

                                need_same_width=[]

                                for x in alllist:
                                    for tempneed in mainproject:
                                        if tempneed.width==x.width:
                                            if tempneed not in alllist and tempneed not in fneed:
                                                need_same_width.append(tempneed)
                                            break
                                    for index in range(len(otherproject)):
                                        for tempneed in otherproject[index]:
                                            if tempneed.width==x.width:
                                                if tempneed not in alllist and tempneed not in fneed:
                                                    need_same_width.append(tempneed)
                                                break

                                break
        storage=[x for x in storage if x not in froll]
    project=[x for x in mainproject if x not in fneed]

    for tempproject in otherproject:#更新其他需求
        tempproject=[x for x in tempproject if x not in fneed]

    data={
        'otherproject':otherproject,
        'project':project,
        'storage':storage,
        'plan':plan,
    }
    return data,total1,total2,rollindex,left_cut

def show(origin_p,prolist,para,totalweight):
    list_rate = []
    for i in range(len(origin_p)):
        prosum=0
        if len(prolist)==0 or totalweight==0:
            break
        for need in origin_p[i]:
            if prolist[i][str(need.width)]!=[]:
                tempsum=sum([x[1] for x in prolist[i][str(need.width)]])
                dist=need.length-tempsum
                prosum=prosum+cal_weight(need.width,tempsum,para)

        print("prosum:"+str(prosum))

        rate=prosum/totalweight*100
        rate_temp = float("%.2f"%(rate))
        list_rate.append(rate_temp)
    return list_rate

def side_process(plan,origin_s,sidebar,sidebarno,sidethread,sym):

    allsidebar=[]
    allsidebar.extend(sidebar)
    allsidebar.extend(sidebarno)

    for roll in origin_s:
        if roll.type!="毛边卷":
            for content in plan[roll.id]:

                tempsum=sum(content['width'])
                remain=roll.width-tempsum
                num=float(remain)/2.0
                if num!=0:
                    content['width'].extend([num,num])
                    content['symbol'].extend([sym['边丝'],sym['边丝']])
        else:
            for content in plan[roll.id]:
                tempsum=sum(content['width'])
                remain=roll.width-tempsum
                remain=remain-sidethread[roll.type].left
                #allsidebar.sort()#边条从小到大排序
                i=2
                maxsum=0
                maxlist=[]
                for subset in combinations_with_replacement(allsidebar,i):#先配边条组合
                    if sum([x.width for x in subset])>maxsum and sum([x.width for x in subset])<=remain:
                        mark=0
                        for x in subset:
                            if x in sidebar and x.length<content['length']:
                                mark=1
                                break
                        if mark==0:
                            maxsum=sum([x.width for x in subset])
                            maxlist=list(subset)
                if maxlist!=[]:
                    for x in maxlist:
                        if x in sidebar:
                            x.length=x.length-content['length']
                        content['width'].append(x.width)
                        content['symbol'].append(x.sym)
                    num=float(remain-maxsum+sidethread[roll.type].left)/2.0
                    content['width'].extend([num,num])
                    content['symbol'].extend([sym['边丝'],sym['边丝']])
    return plan

def plan_process(plan):
    ans={}
    for rollid in plan:
        ans[rollid]=[]
        for content in plan[rollid]:
            tempdic={}
            tempdic['width']=''
            for i in range(len(content['width'])):
                if content['symbol'][i]=='^':
                    tempdic['width']=tempdic['width']+content['symbol'][i]+str(float(content['width'][i]))
                else:
                    tempdic['width']=tempdic['width']+content['symbol'][i]+str(int(content['width'][i]))
            tempdic['length']=content['length']
            ans[rollid].append(tempdic)
    return ans











                    



 




                        



                    



