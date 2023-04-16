
import socket
import pymongo
import time
import threading
import os,struct
import tkinter as tk  
from tkinter import *
from tkinter import messagebox
import shutil,sys

class Server:#服务器类
    def __init__(self):
        #连接数据库
        self.Client=pymongo.MongoClient(host='localhost',port=27017)
        self.db=self.Client.mapsystem#使用mapsystem数据库
        #创建用户文件夹
        if not os.path.exists('.\\user'):#如果没有用户文件夹
            os.makedirs('.\\user')#创建文件夹
        #创建主窗口
        self.isopen=0#服务器是否打开的标志
        self.root=Tk()#创建主窗口
        self.layout()#构件布局
        self.root.protocol("WM_DELETE_WINDOW",self.Exit)#关闭监听
        self.root.mainloop()
        
    def register(self,id,password,user):#注册用户
        if self.verify(id,password)[0]==0:#如果数据库中没有此id
            data={'ID':id,'PassWord':password,'UserName':user,'LastTime':''}#传入的用户信息
            self.collection.insert(data)#存入数据库中的users集合
            os.makedirs('.\\user\\'+id)#创建该用户的数据文件夹
            os.makedirs('.\\user\\'+id+'\\txt')#创建该用户的文本文件夹
            os.makedirs('.\\user\\'+id+'\\image')#创建该用户的图像文件夹
            os.makedirs('.\\user\\'+id+'\\erro')#创建该用户的错误数据文件夹
            self.lb.delete(0,END)
            self.display()
            return 0#表示注册成功
        else:
            return -1#表示ID已经被占用
    
    def verify(self,id,password):#验证密码是否正确,返回值为[状态，用户名]
        self.collection=self.db.users#指定集合
        result=self.collection.find_one({'ID':id})#查询id
        if result==None:#没有查询结果
            return [0,None]#表示没有此用户
        elif password==result['PassWord']:#如果用户输入的密码和查询出的密码一致
            t=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())#获取当前时间
            condition = {'ID':id}  
            result=self.collection.find_one(condition)  
            result['LastTime'] =t 
            self.collection.update(condition, result) #修改上一次登陆时间
            self.lb.delete(0,END)
            self.display()
            return [1,result['UserName']]#表示匹配一致
        elif password!=result['PassWord']:#不一致
            return [-1,None]#表示匹配不一致

    def communicate(self,clientsocket):#负责与客户端的通信
        while True:#循环接受
            msg=clientsocket.recv(1024)#接受客户端发来的消息
            strmsg=msg.decode("utf-8")#将接受的数据解码
            if strmsg=='register':#如果是要注册新用户
                msg_id=clientsocket.recv(1024)#接收账户
                strmsg_id=msg_id.decode("utf-8")
                msg_password=clientsocket.recv(1024)#接收密码
                strmsg_password=msg_password.decode("utf-8")
                msg_user=clientsocket.recv(1024)#接收用户名
                strmsg_user=msg_user.decode("utf-8")
                if self.register(strmsg_id,strmsg_password,strmsg_user)==0:#注册成功
                    str='successful'
                    clientsocket.send(str.encode("utf-8"))#给客户端发送成功标志
                else:#注册不成功
                    str='fail'
                    clientsocket.send(str.encode("utf-8"))#给客户端发送失败标志
            if strmsg=='verify':#如果是要验证登录
                msg_id=clientsocket.recv(1024)#接收账户
                strmsg_id=msg_id.decode("utf-8")
                msg_password=clientsocket.recv(1024)#接收密码
                strmsg_password=msg_password.decode("utf-8")
                result=self.verify(strmsg_id,strmsg_password)#调用验证函数，得到判断结果列表
                if result[0]==0:#没有这个用户
                    clientsocket.send('nothing'.encode("utf-8"))#给客户端发送没有此用户
                if result[0]==-1:#密码不匹配
                    clientsocket.send('wrong'.encode("utf-8"))#给客户端发送密码错误
                if result[0]==1:#匹配成功
                    clientsocket.send('successful'.encode("utf-8"))#给客户端发送匹配成功
                    time.sleep(0.1)
                    clientsocket.send(result[1].encode("utf-8"))#并且发送用户名
            if strmsg=='erro':#如果是传输错误数据文件
                msg_id=clientsocket.recv(1024).decode("utf-8")#接受id
                msg_filename=clientsocket.recv(1024).decode("utf-8")#接受文件名
                file=open('.\\user\\'+msg_id+'\\erro\\'+msg_filename,'w')#在该用户的目录下创建一个文件
                while True:
                    msg_content=clientsocket.recv(1024).decode("utf-8")#接受内容
                    if msg_content=='EOF':#传输完成
                        break
                    file.write(msg_content)#写入数据
                file.close()#关闭文件
            if strmsg=='txt':#如果是传输文本文件
                msg_id=clientsocket.recv(1024).decode("utf-8")#接受id
                msg_filename=clientsocket.recv(1024).decode("utf-8")#接受文件名
                file=open('.\\user\\'+msg_id+'\\txt\\'+msg_filename,'w')#在该用户的目录下创建一个文件
                while True:
                    msg_content=clientsocket.recv(1024).decode("utf-8")#接受内容
                    if msg_content=='EOF':#传输完成
                        break
                    file.write(msg_content)#写入数据
                file.close()#关闭文件
            if strmsg=='image':#如果传输的是图像文件
                msg_id=clientsocket.recv(1024).decode("utf-8")#接受id
                fileinfo_size = struct.calcsize('128sq')
                buf = clientsocket.recv(fileinfo_size)  # 接收图片名
                if buf:
                    filename, filesize = struct.unpack('128sq', buf)
                    fn = filename.decode().strip('\x00')
                    fp = open('.\\user\\'+msg_id+'\\image\\'+fn, 'wb')#在相应的位置打开一个文件写入数据
                    while True:
                        msg_content=clientsocket.recv(1024)#接受内容
                        if msg_content=='EOF':#传输完成
                            break
                        fp.write(msg_content)  # 写入图片数据
                    fp.close()

    def layout(self):#服务器界面布局
        self.root.title('服务器管理界面')#设置窗口标题
        self.root.geometry('600x600')#设置窗口大小
        self.root.resizable(width=False,height=False)#大小不可变
        self.button1=tk.Button(self.root,text='启动服务器',height=1,width=10,font=('华文行楷',14),command=self.start)
        self.button1.place(x=150,y=530)
        self.button2=tk.Button(self.root,text='关闭服务器',height=1,width=10,font=('华文行楷',14),command=self.stop)
        self.button2.place(x=400,y=530)
        self.label1=tk.Label(self.root,text='UserList',height=1,width=8,font=('楷体',16),background='gray')
        self.label1.place(x=270,y=25)
        self.label2=tk.Label(self.root,text='OFF',height=1,width=8,font=('楷体',14),background='red')
        self.label2.place(x=280,y=535)
        self.lb = tk.Listbox(self.root,height=25,width=78)
        self.lb.place(x=25,y=50)
        self.display()#展示用户列表
        self.lb.bind("<Double-Button-1>",self.delete)#双击左键删除用户

    def start(self):#启动或停止服务器
        if self.isopen==0:#如果是关闭状态，则开启
            self.isopen=1#状态改变
            self.label2.config(text='ON',background='green')
            t=threading.Thread(target=self.link)#开辟一个线程连接客户端
            t.start()
        else:
            messagebox.askokcancel('提示','服务器已启动')
        
    def stop(self):#关闭服务器
        if self.isopen==1:#如果已经打开
            self.isopen=0#状态改变
            self.label2.config(text='OFF',background='red')
            self.Client.close()#关闭服务器
        else:
            messagebox.askokcancel('提示','服务器已关闭')
    
    def link(self):#连接客户端
        #创建服务端的socket对象socketserver
        self.socketserver = socket.socket()
        self.host = '192.168.73.1'#本机ip地址
        self.port = 5000
        self.socketserver.bind((self.host, self.port))#绑定地址（包括ip地址和端口号）
        self.socketserver.listen(5)#设置监听                
        #启动客户端和服务端的交互
        while True:
            clientsocket,addr = self.socketserver.accept()#等待客户端的连接,accept()函数会返回一个元组,元素1为客户端的socket对象，元素2为客户端的地址(ip地址，端口号)
            t=threading.Thread(target=self.communicate,args=(clientsocket,))#为一个客户端开辟一个线程开辟一个线程
            t.start()#启动线程
    
    def display(self):#显示用户列表
        self.collection=self.db.users#指定集合
        results = self.collection.find()#查询所有用户  
        for result in results:
            self.lb.insert('end', result['ID']+'      '+result['UserName']+'      '+result['PassWord']+'      '+result['LastTime'])#插入数据
        
    def delete(self,event):#注销用户
        index=self.lb.curselection()#记录被选中的序号
        content=self.lb.get(index)#获取这一项的内容
        self.collection=self.db.users#指定集合
        i=0
        for i in range(len(content)):
            if content[i]==' ':
                break
        id=content[0:i]#截取用户id
        if messagebox.askokcancel('提示','确定要注销此用户吗？')==True:
            shutil.rmtree('.\\user\\'+id)#删除该用户的文件夹
            self.collection.remove({'ID':id})#从数据库中删除
            self.lb.delete(0,END)
            self.display()#刷新页面

    def Exit(self):#退出
        self.root.withdraw()      
        self.Client.close()
        sys.exit()
        


Server()

