import pymysql
import jieba
user = "root"
passwd = "NUDTpdl@"
f = open('logcontent.txt','w')
conn = pymysql.connect(host="127.0.0.1",user=user,passwd=passwd,db="contentsplitword",charset='utf8mb4' )
conn.set_charset('utf8')
conn.autocommit(1)
cur=conn.cursor()
select_sqltotal="select content,date from totaldata where content!=''"
update_sql="update totaldata set contentsplit=\'%s\' where date=\'%s\'"
stopw = [line.strip().decode('utf-8') for line in open('E:\\pla\\stopword.txt', 'rb').readlines()]
def segmentWord(cont):
    c = []
    for i in cont:
        a = list(jieba.cut(i))
        b = " ".join(a)
        c.append(b)
    return c
def datepre():
    cur.execute(select_sqltotal)

    totalcontent = cur.fetchall()
    array=[]
    arraytime=[]
    for singcontent in totalcontent:
        array.append(singcontent[0])
        arraytime.append(singcontent[1])
    # print(totalcontent[0][1])
    segeword=segmentWord(array)
    content = stopwordfilter(segeword)
    for i in range(len(content)):
        try:
            cur.execute(update_sql%(content[i],arraytime[i]))
            if i%100==0:
                print("%d handled"%(i))
        except:
            print(arraytime[i],file=f)
            pass
def stopwordfilter(contentarray):
    outstrarray=[]
    for content in contentarray:
        strarray = content.split(' ')
        #print(strarray)

        outstr = ''
        for word in strarray:

            if word not in stopw:
                if word != '\t':
                    outstr += word
                    outstr += " "
        outstrarray.append(outstr)
    return outstrarray
datepre()
