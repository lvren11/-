import csv
import copy
from func import *
import traceback
import datetime


def program(REMAIN_MIN_WIDTH, THICKNESS, POSITIVE_ERROR_PERCENT, NEGATIVE_ERROR_PERCENT, LEFT_FUR, RIGHT_FUR, LEFT_CUT, RIGHT_CUT, LEFT_STOCK, RIGHT_STOCK,  MIN_LENGTH, path_need, path_roll, Need_encoding, Roll_encoding, length_difference, mode):
    aa=datetime.datetime.now()#开始时间点
    
    
    if mode == "宽度优先":
        mode = 0
    else:
        mode = 1

    SIDE_THREAD = {#边丝
        '毛边卷':Interval(LEFT_FUR, RIGHT_FUR),
        '切边卷':Interval(LEFT_CUT, RIGHT_CUT),
        '库存':Interval(LEFT_STOCK, RIGHT_STOCK),
    }
    
    NEED_FILE_PATH = path_need
    ROLL_FILE_PATH = path_roll

    para=[7.65,float(THICKNESS),1000]

    mylist=[]

    try:
        

        program_ok = True
        cproject,projectsym,sidebar,sidebarsym,sidebar_scale=get_project(NEED_FILE_PATH, POSITIVE_ERROR_PERCENT,NEGATIVE_ERROR_PERCENT, Need_encoding,para)

        sidebar_noclient=[]
        #m=int(sidebar_scale[0].width/2/10)
        #n=int(sidebar_scale[0].weight/2/10)
        for i in range(int(sidebar_scale[0].width),int(sidebar_scale[0].weight)+1,10):
            bar=Bar_no_client(i,sidebar_scale[0].sym)
            sidebar_noclient.append(bar)
        
        

        SIDE_BAR = Interval(sidebar_scale[0].width*2, sidebar_scale[0].weight*2)#边条

        sidebarlist=[]
        for ilist in sidebar:
            sidebarlist.extend(ilist)

        sym={}

        sym['项目']=projectsym

        sym['边丝']='^'
        sym['余材']=sym['项目'][-1]

        '''
        sym={
            "主项目":'+',
            "次项目":'#',
            "第三项目":'$',
            "余材":'&',
            "边条":'=',
            "指定边条":'*',
            "边丝":'^',
        }
        '''

        tempmain=0
        temptotal=0
        tempprolist=[]
        tempplan={}
        tempsum=0
        tempidlist=[]
        doneflag=0
        templeftcut=0
        temprecord={}
        temprollindex=0
        tempsorted_storage=[]
        temp_origin_plan={}

        for i in range(1,7):

            method=i

            print(i)
        
            project=[]
            storage=[]
            idlist=[]
            originidlist=[]
            sorted_storage=[]
            left_cut=0

            sum1=0
            sum2=0
            sum3=0

            record={
                '1':[],
                '2':[],
                '3':[],
                '4':[]
            }

            project,_,_,_,_=get_project(NEED_FILE_PATH, POSITIVE_ERROR_PERCENT,NEGATIVE_ERROR_PERCENT, Need_encoding,para)
            storage=get_storage(ROLL_FILE_PATH, SIDE_THREAD,SIDE_BAR,NEGATIVE_ERROR_PERCENT, Roll_encoding,para)
            
            for x in storage:
                originidlist.append(x.id)
                idlist.append(x.id)

            rollindex=0

            roll_length = []
            for i in range(len(storage)):
                roll_length.append(int(storage[i].length))
            #print(f'[{project[0][0].lengthscale.left},{project[0][0].lengthscale.right}]')
            #print(f'[{storage[0].widthscale.left},{storage[0].widthscale.right}]')

            #读取需求和原材料
            print(project)
            for list in project:
                list.sort(key=lambda x:x.width,reverse=True)
            storage.sort(key=lambda x:x.width,reverse=True)

            #拷贝初始需求和原材料
            origin_storage=copy.deepcopy(storage)
            origin_project=copy.deepcopy(project)

            #初始化方案字典
            storage.sort(key=lambda x:(x.widthscale.right,x.length,x.id),reverse=True)
            plan={}
            for roll in storage:
                plan[roll.id]=[]

            #取出次需求
            otherproject=[]
            for p in range(1,len(project)):
                otherproject.append(project[p])

            #从需求角度初始化方案
            prolist=[]
            for pro in origin_project:
                tempdic={}
                for need in pro:
                    tempdic[str(need.width)]=[]
                prolist.append(tempdic)

            # print(len(project[0]))
            # print(len(storage))

            #直接匹配
            data,total,rollindex=direct_match(project[0],storage,para,MIN_LENGTH,plan,sym,idlist,rollindex,prolist,record,'1')
            sum1=sum1+total
            # print(total)
            print(data['plan'])
            print(len(data['project']))
            print(len(data['storage']))
            for x in data['project']:
                print(f'{x.width}  {x.length}  {x.lengthscale.left}  {x.lengthscale.right}')
            
            for x in data['storage']:
                print(f'{x.width}  {x.length} ')


            """ firstlist=copy.deepcopy(idlist)
            firstindex=rollindex
            idlist=copy.deepcopy(originidlist)
            rollindex=0 """
            


            project1=data['project']
            storage1=data['storage']
            plan1=data['plan']

            """ #将前几步生成的方案加入需求方案
            for roll in origin_storage:
                for templist in plan1[roll.id]:
                    for width in templist['width']:
                        if str(width) in prolist[0]:
                            prolist[0][str(width)].append((roll.id,templist['length'])) """

            #宽度匹配
            if mode==1:
                data,total,total2,rollindex=length_match(project1,storage1,para,MIN_LENGTH,plan1,REMAIN_MIN_WIDTH,sym,method,otherproject,prolist,idlist,rollindex,record,'2')
                sum1=sum1+total
                sum2=sum2+total2
            elif mode==0:
                total2,data,total,rollindex,left_cut=width_match(project1,otherproject,storage1,para,MIN_LENGTH,plan1,REMAIN_MIN_WIDTH,sym,method,length_difference,prolist,idlist,rollindex,sorted_storage,left_cut,record,'2')
            # print(total)
                sum1=sum1+total
                sum2=sum2+total2
                otherproject=data['otherproject']
            print(data['plan'])
            print(len(data['project']))
            print(len(data['storage']))

            for x in data['project']:
                print(f'{x.width}  {x.length}  {x.lengthscale.left}  {x.lengthscale.right}')
            
            for x in data['storage']:
                print(f'{x.width}  {x.length} ')

            project2=data['project']
            storage2=data['storage']
            plan2=data['plan']

            print("leftcut:"+str(left_cut))

            #长度匹配
            if mode==1:
                total2,data,total,rollindex,left_cut=width_match(project2,otherproject,storage2,para,MIN_LENGTH,plan2,REMAIN_MIN_WIDTH,sym,method,length_difference,prolist,idlist,rollindex,sorted_storage,left_cut,record,'3')
                sum1=sum1+total
                sum2=sum2+total2
                otherproject=data['otherproject']
            #elif mode==0:
                #data,total,total2,rollindex=length_match(project2,storage2,para,MIN_LENGTH,plan2,REMAIN_MIN_WIDTH,sym,method,otherproject,prolist,idlist,rollindex,record,'3')
            # print(total)
                #sum1=sum1+total
                #sum2=sum2+total2
            print(data['plan'])
            print(len(data['project']))
            print(len(data['storage']))

            print("leftcut:"+str(left_cut))

            for x in data['project']:
                print(f'{x.width}  {x.length}  {x.lengthscale.left}  {x.lengthscale.right}')

            for x in data['storage']:
                print(f'{x.width}  {x.length} ')

            project3=data['project']
            storage3=data['storage']
            plan3=data['plan']
            

            """ print(idlist)

                
            for x in firstlist:
                if x not in idlist[:rollindex]:
                    for idx in range(rollindex,len(idlist)):
                        if x==idlist[idx]:
                            temp=idlist[rollindex]
                            idlist[rollindex]=x
                            idlist[idx]=temp
                            rollindex=rollindex+1
                            break

            print(idlist) """

            print("leftcut:"+str(left_cut))



            #全匹配
            data,total1,total2,rollindex,left_cut=all_match(project3,otherproject,storage3,prolist,project,para,MIN_LENGTH,plan3,REMAIN_MIN_WIDTH,sym,method,idlist,rollindex,sorted_storage,left_cut,record,'4')
            sum1=sum1+total1
            sum2=sum2+total2

            project4=data['project']
            storage4=data['storage']
            plan4=data['plan']

            """  #全匹配
            if len(data['project'])!=0:
                data,total1,total2=all_match(project3,otherproject,storage3,prolist,project,para,POSITIVE_ERROR_PERCENT,NEGATIVE_ERROR_PERCENT,MIN_LENGTH,plan3,REMAIN_MIN_WIDTH,sym,method,1)
                sum1=sum1+total1
                sum2=sum1+total2 """

            print(plan)

            origin_plan=copy.deepcopy(data['plan'])

            m=0

            print(idlist)
            print(sorted_storage)

            for id in idlist:
                print(id)
                if plan4[id]==[]:
                    break
                if m==0:
                    print(1)
                    m=1
                    lastid=id
                    continue
                if id in sorted_storage:
                    print(2)
                    lastid=id
                    continue
                if plan4[lastid][-1]['width']==plan4[id][0]['width']:
                    print(3)
                    print(plan4[lastid][-1]['width'])
                    left_cut=left_cut+1
                    lastid=id
                lastid=id

            
            #分配指定边条规格
            plan=side_process(data['plan'],origin_storage,sidebarlist,sidebar_noclient,SIDE_THREAD,sym)

            # print(len(data['project']))
            # print(len(data['storage']))
            #print(prolist)

            print("leftcut:"+str(left_cut))




            print("主需求：")
            for i in data['project']:
                print(f'{i.width}  {i.length}')

            print("库存：")
            for i in data['storage']:
                print(f'{i.width}  {i.length}')

            #print("其他需求：")
            #for i in data['otherproject']:
                #print(f'{i.width}  {i.length}')

            # print(sum1)
            # print(sum2)

            #计算使用的原材料总重量
            for roll in origin_storage:
                flag=0
                for i in data['storage']:
                    if roll.id==i.id:
                        sum3=sum3+cal_weight((roll.length-i.length),i.width,para)
                        flag=1
                        break
                if flag==0:
                    sum3=sum3+cal_weight(roll.length,roll.width,para)

            print(sum3)

            print("主项目率：")
            main_rate=float("%.2f" %(sum1/sum3*100))
            print("%.2f" %(sum1/sum3*100))

            print("总项目率：")
            all_rate = float("%.2f" %((sum1+sum2)/sum3*100))
            print("%.2f" %((sum1+sum2)/sum3*100))

            mylist.append((sum1,sum2,sum3))

            if main_rate>tempmain:
                tempplan=plan
                tempmain=main_rate
                temptotal=all_rate
                tempprolist=prolist
                tempsum=sum3
                tempidlist=idlist
                templeftcut=left_cut
                temprecord=record

                temprollindex=rollindex
                tempsorted_storage=sorted_storage
                temp_origin_plan=origin_plan
            elif main_rate==tempmain:
                if all_rate>temptotal:
                    tempplan=plan
                    tempmain=main_rate
                    temptotal=all_rate
                    tempprolist=prolist
                    tempsum=sum3
                    tempidlist=idlist
                    templeftcut=left_cut
                    temprecord=record

                    temprollindex=rollindex
                    tempsorted_storage=sorted_storage
                    temp_origin_plan=origin_plan

            if len(data['project'])==0:
                doneflag=1

        #显示需求结果：需求宽度 需求长度 分配长度 差值
        if len(tempprolist)==0:
            for pro in origin_project:
                tempdic={}
                for need in pro:
                    tempdic[str(need.width)]=[]
                tempprolist.append(tempdic)

        print(tempprolist)

        list_rate = show(origin_project,tempprolist,para,tempsum)

        """ templist=copy.deepcopy(tempidlist)

        origin_sorted_stroage=copy.deepcopy(tempsorted_storage)

        followlist=[]

        for index in range(temprollindex-1):
            if tempidlist[index+1] in tempsorted_storage:
                followlist.append(templist[index])

        for idx1 in range(temprollindex):
            maxsim=0
            if templist[idx1] not in followlist:
            #if templist[idx1] not in tempsorted_storage and (idx1<temprollindex-1 and templist[idx1+1] not in tempsorted_storage):#后面没有跟着的卷
                tempwidth1=temp_origin_plan[templist[idx1]][-1]['width']
                tempidx=idx1
                print(templist[idx1],end=' ')
                print(tempwidth1)
                for idx2 in range(temprollindex):#遍历所有母卷
                    if idx1==idx2 or templist[idx2] in tempsorted_storage :#母卷已经跟着其他母卷 or 就是自己
                        continue

                    tempsim=0

                    tempwidth2=temp_origin_plan[templist[idx2]][0]['width']

                    print(templist[idx2],end=' ')

                    print(tempwidth2)
                    for x in tempwidth1:#计算相似度
                        if x in tempwidth2 or int(x) in tempwidth2:
                            tempsim=tempsim+1
                    if tempsim>maxsim:
                        maxsim=tempsim
                        tempidx=idx2
                    elif tempsim==maxsim:
                        if len(tempwidth2)==1:
                            maxsim=tempsim
                            tempidx=idx2
                    print("maxsim:"+str(maxsim))
                
                if maxsim!=0:
                    tempsorted_storage.append(templist[tempidx])
                    tempid=templist[tempidx]
                    idx1_real=tempidlist.index(templist[idx1])
                    idx2_real=tempidlist.index(templist[tempidx])
                    print(idx2_real)
                    tempwidth1=temp_origin_plan[templist[idx1]][-1]['width']
                    tempwidth2=temp_origin_plan[templist[tempidx]][0]['width']

                    if tempwidth1==tempwidth2:
                        templeftcut=templeftcut+1

                    while 1:
                        print(tempidlist[idx1_real],end=' ')
                        print(tempid)
                        tempidlist.remove(tempid)
                        tempidlist.insert(idx1_real+1,tempid)

                        idx2_real=idx2_real+1
                        print(idx2_real)
                        if idx2_real>=len(tempidlist):
                            break
                        tempid=tempidlist[idx2_real]
                        idx1_real=idx1_real+1

                        print(tempidlist)

                        if tempid not in tempsorted_storage:
                            break """

        ans=plan_process(tempplan)
        # print(tempmain)
        # print(temptotal)
        print(ans)

        if tempmain!=0:
            f=1
        else:
            f=0
    except Exception as e:
        print(traceback.format_exc())
        ans = {}
        tempprolist = [0,0]
        list_rate = []
        temptotal = 0.0
        #f = 0
        doneflag=0
        roll_length = []
        program_ok = False
        tempidlist=[]
        templeftcut=0

    bb=datetime.datetime.now()#结束时间点

    cc=bb-aa


    print(list_rate)

    print("templeftcut"+str(templeftcut))

    print(cc)

    print(temprecord)

    file=open('./log.txt','w')
    file.truncate(0)

    cc=str(cc).split(':')

    file.write('运行时间: '+str(cc[0])+'时'+str(cc[1])+'分'+str(cc[2])+'秒'+'\n')

    for i in range(1,5):
        file.write('###############第'+str(i)+'步###############\n\n')
        for record in temprecord[str(i)]:
            file.write('卷号：'+str(record['roll'].id)+'；卷宽度：'+str(record['roll'].width)+' ')
            width_line='；宽度：'
            for i in range(len(record['content']['width'])):
                if record['content']['symbol'][i]=='^':
                    break
                else:
                    width_line=width_line+record['content']['symbol'][i]+str(int(record['content']['width'][i]))

            file.write(width_line+'；长度：'+str(record['content']['length'])+'\n\n')


    file.close()

    print()
    print(tempsum)

    print("mylist:",end='')
    print(mylist)
    print()


    return ans,tempprolist,list_rate,temptotal,doneflag,roll_length,program_ok,tempidlist,templeftcut

















    
