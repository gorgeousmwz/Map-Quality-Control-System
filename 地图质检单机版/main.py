import os
from tkinter import *
from tkinter import scrolledtext
from tkinter.simpledialog import askstring
from tkinter.ttk import *
import tkinter as tk  
from tkinter import ttk
import tkinter.filedialog as tkf 
from tkinter import messagebox
from PIL import Image, ImageTk
import sys
from numpy import tile

class Main:#主程序框架类
    def __init__(self):#构造函数
        self.image=None#图像数据（初始设为空）
        self.txt=None#文本数据（初始设为空）
        self.file=None#错误文件对象（初始设为空）
        self.x=-1#存储点击坐标（初始为-1）
        self.y=-1
        self.index=1#记录是第几条错误
        self.erro=[]#存储所有错误信息
        self.root=Tk()#创建主窗口
        self.layout()#构件布局
        self.root.mainloop()

    def layout(self):#主界面的初始布局设置
         self.root.title('地图质检')#设置窗口标题
         self.root.geometry('1200x600')#设置窗口大小
         self.root.resizable(width=False,height=False)#大小不可变
         #菜单选项设置
         self.mainmenu=Menu(self.root)#创建主菜单
         self.menuData=Menu(self.mainmenu)#菜单分组
         self.mainmenu.add_cascade(label='数据文件',menu=self.menuData)#添加一个文件分组
         self.menuData.add_command(label='打开图像数据',command=self.openImageFile)#在下面添加选项
         self.menuData.add_command(label='打开文本数据',command=self.openDataFile)
         self.menuErro=Menu(self.mainmenu)
         self.mainmenu.add_cascade(label='错误信息',menu=self.menuErro)
         self.menuErro.add_command(label='新建错误文件',command=self.newErroFile)
         self.menuErro.add_command(label='打开错误文件',command=self.openErroFile)
         self.menuErro.add_command(label='删除错误文件',command=self.deleteErroFile)
         self.menuOther=Menu(self.mainmenu)
         self.mainmenu.add_cascade(label='其他',menu=self.menuOther)
         self.menuOther.add_command(label='帮助',command=self.Help)
         self.menuOther.add_command(label='退出',command=self.Exit)
         self.root.config(menu=self.mainmenu)#设为菜单
         #分割线设置
         self.sep=Separator(self.root,orient=VERTICAL)#竖直分割线
         self.sep.pack(padx=10,pady=3,fill='y',expand=True)
         #框架设置
         self.frame1=tk.Frame(self.root,bd=1,height=550,width=550,relief='solid')#此框架为显示地图窗口
         self.frame1.place(x=25,y=35)
         self.frame2=tk.Frame(self.root,bd=1,height=350,width=550,relief='solid')#此框架为添加错误记录窗口
         self.frame2.place(x=625,y=10)
         self.frame3=tk.Frame(self.root,bd=1,height=220,width=550,relief='solid')#此框架为查询错误窗口
         self.frame3.place(x=625,y=370)
         #标签设置
         self.label1=tk.Label(self.root,text='文件名:',height=1,width=6,font=('华文行楷',12))#这里的高度单位为行，宽单位为字符
         self.label1.place(x=25,y=10)
         self.label2=tk.Label(self.root,text='',anchor='w',height=1,width=40,font=('华文行楷',12))#设置为左对齐
         self.label2.place(x=80,y=10)
         self.label3=tk.Label(self.root,text='错误坐标:',anchor='center',height=1,width=8,font=('华文行楷',12))
         self.label3.place(x=635,y=20)
         self.label4=tk.Label(self.root,text='错误类型:',anchor='center',height=1,width=8,font=('华文行楷',12))
         self.label4.place(x=635,y=60)
         self.label5=tk.Label(self.root,text='错误描述:',anchor='center',height=1,width=8,font=('华文行楷',12))
         self.label5.place(x=635,y=100)
         self.label6=tk.Label(self.root,text='错误查询:',anchor='center',height=1,width=8,font=('华文行楷',12))
         self.label6.place(x=635,y=380)
         self.label7=tk.Label(self.root,text='错误信息:',anchor='center',height=1,width=8,font=('华文行楷',12))
         self.label7.place(x=635,y=420)
         self.label8=tk.Label(self.root,text='X:',anchor='center',height=1,width=2,font=('华文行楷',12))
         self.label8.place(x=750,y=20)
         self.label9=tk.Label(self.root,text='Y:',anchor='center',height=1,width=2,font=('华文行楷',12))
         self.label9.place(x=950,y=20)
         self.label10=tk.Label(self.root,text='',anchor='center',height=1,width=8,font=('华文行楷',12),fg='red')
         self.label10.place(x=850,y=20)
         self.label11=tk.Label(self.root,text='',anchor='center',height=1,width=8,font=('华文行楷',12),fg='red')
         self.label11.place(x=1050,y=20)
         self.label12=tk.Label(self.root,text='1/1',anchor='center',height=1,width=4,font=('华文行楷',14),bg='white')
         self.label12.place(x=890,y=300)
         #复选框设置
         self.combobox=ttk.Combobox(self.root,height=3,width=20,values=['名称错误','坐标错误','属性错误','其他错误'])
         self.combobox.place(x=750,y=60)
         #文本框设置
         self.text1=scrolledtext.ScrolledText(self.root,height=8,width=50)
         self.text1.place(x=750,y=100)
         self.text2=Text(self.root,height=1,width=30)
         self.text2.place(x=750,y=380)
         self.text3=scrolledtext.ScrolledText(self.root,height=10,width=50)
         self.text3.place(x=750,y=420)
         #按钮设置
         self.button1=tk.Button(self.root,text='添加',height=1,width=8,font=('华文行楷',12),command=self.addErro)
         self.button1.place(x=750,y=250)
         self.button2=tk.Button(self.root,text='保存',height=1,width=8,font=('华文行楷',12),command=self.saveErro)
         self.button2.place(x=875,y=250)
         self.button3=tk.Button(self.root,text='删除',height=1,width=8,font=('华文行楷',12),command=self.deleteErro)
         self.button3.place(x=1000,y=250)
         self.button4=tk.Button(self.root,text='上一条',height=1,width=8,font=('华文行楷',12),command=self.latter)
         self.button4.place(x=750,y=300)
         self.button5=tk.Button(self.root,text='下一条',height=1,width=8,font=('华文行楷',12),command=self.next)
         self.button5.place(x=1000,y=300)
         self.button6=tk.Button(self.root,text='查询',height=1,width=8,font=('华文行楷',12),command=self.search)
         self.button6.place(x=980,y=375) 
    
    def openImageFile(self):#打开图像文件并显示
        for data in self.frame1.winfo_children():
            data.destroy()  # 清理已打开的数据
        filename=tkf.askopenfilename()#打开文件
        self.label2.config(text=filename)#在上方显示文件路径
        if filename!='':
            im=Image.open(filename)#打开图片
            im=im.resize((545,545),Image.ANTIALIAS)#调整大小
            self.image=ImageTk.PhotoImage(im)#将图像存入全局变量中
            label_image=tk.Label(self.frame1,image=self.image)#将图像借助标签显示
            label_image.pack()
            label_image.bind("<Double-Button-1>",self.getXY)#双击左键获取坐标

    def openDataFile(self):#打开数据文件并显示
        for data in self.frame1.winfo_children():
            data.destroy()  # 清理已打开的数据
        filename=tkf.askopenfilename()#打开文件
        self.label2.config(text=filename)#在上方显示文件路径
        with open(filename, encoding='utf-8', errors='ignore') as f:
            content = f.readlines()  # 按行读取
        self.txt=content#将文本数据存到全局变量中
        # 将读取到的内容放入Listbox
        lb = tk.Listbox(self.frame1,height=30,width=80)
        lb.pack()
        for line in content:
            lb.insert('end', line)
        lb.bind("<Double-Button-1>",self.getXY)#双击左键获取坐标
    
    def newErroFile(self):#新建错误文件
        if self.erro!=[]:
            if messagebox.askokcancel('提示', '确定打开新的错误文件吗？\n如果错误信息未保存\n信息会丢失')==False:
                return None
        self.erro=[]#错误列表清空
        self.index=1#错误索引归零
        self.label12.config(text=str('1/1'))#重置页面
        self.clear_erro()
        if self.file!=None:#若果已打开文件则关闭
            self.file.close()
        filename = askstring('新建错误文件', prompt='输入您创建的文件名', initialvalue='Erro')#打开对话框让用户输入文件名
        self.file=open(filename+'.txt','a+',encoding='utf-8')#新建文件
        if self.file!=None:#新建成功，给出提示
            messagebox.askokcancel('提示', '成功新建文件')
        else:#新建失败，给出提示
            messagebox.askokcancel('提示', '新建文件失败')
    
    def openErroFile(self):#打开错误文件
        if self.erro!=[]:
            if messagebox.askokcancel('提示', '确定打开新的错误文件吗？\n如果错误信息未保存\n信息会丢失')==False:
                return None
        self.erro=[]#错误列表清空
        self.index=1#错误索引归零
        self.label12.config(text=str('1/1'))#重置页面
        self.clear_erro()
        if self.file!=None:#如果已经有文件打开就将其关闭
            self.file.close()
        filename=tkf.askopenfilename()#打开文件对话框，储存文件名
        self.file=open(filename,'a+',encoding='utf-8')#以追加的方式打开文件
        if self.file!=None:#打开成功，给出提示
           messagebox.askokcancel('提示', '成功打开文件')
        else:#打开失败，给出提示
            messagebox.askokcancel('提示', '打开文件失败')
     
    def deleteErroFile(self):#删除错误文件
        filename =tkf.askopenfilename()  # 文件路径
        if messagebox.askokcancel('提示', '是否删除'+filename)==True:
            os.remove(filename)#删除文件  
            if os.path.exists(filename):  # 如果文件存在
                messagebox.askokcancel('提示', '删除文件失败')
            else:
                messagebox.askokcancel('提示', '删除文件成功')

    def Help(self):#帮助
        messagebox.showinfo('帮助','作者：马文卓\n版本:1.0\n语言:Python\n库:tkinter')
    
    def Exit(self):#退出
        if messagebox.askokcancel('提示', '您确定退出程序吗？')==True:#弹出提示框等待选择
           if self.file!=None:#如果文件还未关闭，则关闭文件
               self.file.close()
           self.root.withdraw()#如果确认则退出窗口
           sys.exit() #退出程序  
    
    def getXY(self,event):#获取点击处坐标，并显示
        self.x=event.x#存储坐标
        self.y=event.y
        self.label10.config(text=str(self.x))#改变标签中的数值
        self.label11.config(text=str(self.y))

    def addErro(self):#添加错误到self.erro
        if self.x>=0 and self.y>=0:#坐标合理时
          erro_type=self.combobox.get()#获取错误类型
          erro_detail=self.text1.get(1.0,END)#获取错误描述
          self.erro+=[[self.x,self.y,erro_type,erro_detail]]#加入一条错误
          self.clear_erro()#清空
          self.index=len(self.erro)+1
          self.label12.config(text=str(str(self.index)+'/'+str(len(self.erro)+1)))#更新下面的页面信息
        else:
            messagebox.askokcancel('提示', '请双击图像以获得一个合理的坐标')

    def saveErro(self):#保存错误文件
        if self.file==None:#没有新建或者打开文件
            filename=tkf.asksaveasfilename()#弹出保存文件对话框
            if filename=='':#如果没有选择文件
                return None
            self.file=open(filename,'a+',encoding='utf-8')
        for i in range(len(self.erro)):
            self.file.write('('+str(self.erro[i][0])+','+str(self.erro[i][1])+')    '+self.erro[i][2]+'    '+self.erro[i][3])#写入信息
        messagebox.askokcancel('提示', '文件保存成功')
        self.clear_erro()
        self.erro=[]
        self.file.close()
        self.file=None
        self.index=1
        self.label12.config(text=str('1/1'))#重置页面

    def deleteErro(self):#删除此条错误信息
        if len(self.erro)==0:#如果没有错误信息
            messagebox.askokcancel('提示', '无错误信息')
        elif len(self.erro)==self.index:#如果是最后一项错误信息，则特殊处理（清空页面）
            self.erro.pop(self.index-1)
            self.clear_erro()#清空界面
            self.label12.config(text=str(self.index)+'/'+str(len(self.erro)+1))#更新下面的页面信息
        else:
            if self.index>=len(self.erro)+1:
               messagebox.askokcancel('提示', '此条信息未编辑')
            else:
               print(self.index)
               self.erro.pop(self.index-1)
               self.label12.config(text=str(self.index)+'/'+str(len(self.erro)+1))#更新下面的页面信息
               self.set_erroinface(self.erro[self.index-1][0],self.erro[self.index-1][1],self.erro[self.index-1][2],self.erro[self.index-1][3])#更新界面

    def latter(self):#上一条
        if self.index==1:
            messagebox.askokcancel('提示', '已经是第一条')
        else:
            self.index-=1
            self.label12.config(text=str(self.index)+'/'+str(len(self.erro)+1))#更新下面的页面信息
            self.set_erroinface(self.erro[self.index-1][0],self.erro[self.index-1][1],self.erro[self.index-1][2],self.erro[self.index-1][3])#更新界面

    def next(self):#下一条
        if self.index==len(self.erro)+1:
                messagebox.askokcancel('提示', '已经是最后一条')
        else:
            if self.index==len(self.erro):#如果是倒数第二条，则清空界面（最后一条还未编辑）
                self.index+=1
                self.label12.config(text=str(self.index)+'/'+str(len(self.erro)+1))#更新下面的页面信息
                self.clear_erro()
            else:
                self.index+=1
                self.label12.config(text=str(self.index)+'/'+str(len(self.erro)+1))#更新下面的页面信息
                self.set_erroinface(self.erro[self.index-1][0],self.erro[self.index-1][1],self.erro[self.index-1][2],self.erro[self.index-1][3])#更新界面

    def search(self):#在已经打开的错误文件和已经添加的错误信息中查询错误信息
        self.text3.delete(1.0,END)#清空展示框
        search_content=self.text2.get(1.0,END)#获取输入的关键词
        search_content=search_content[0:len(search_content)-1]#上面读取的字符串最后带有\n一定要去除
        search_result=[]#储存查询结果
        if self.file!=None:#如果有错误文件打开，则先在错误文件中查询
            self.file.seek(0,0)#将指针调到文件开始
            erro_content=self.file.readlines()#按行读取
            for i in range(len(erro_content)):
                if erro_content[i].find(search_content)>=0:#如果关键字被包含在这条错误信息中
                    search_result+=[erro_content[i]]
        for i in range(len(self.erro)):#遍历所有错误信息
            #将每条错误信息串联起来便于查询，中间用空格隔开避免数字连接造成查询出现偏差
            erro_content=str(self.erro[i][0])+'  '+str(self.erro[i][1])+'  '+self.erro[i][2]+'  '+self.erro[i][3]
            if erro_content.find(search_content)>=0:#如果关键字被包含在这条错误信息中
                search_result+=['('+str(self.erro[i][0])+','+str(self.erro[i][1])+')    '+self.erro[i][2]+'    '+self.erro[i][3]]
        for i in range(len(search_result)):#展示查询结果
            self.text3.insert(END,search_result[i])

    def clear_erro(self):#清空错误区
        self.x=-1
        self.y=-1
        self.label10.config(text='')
        self.label11.config(text='')
        self.combobox.set('')
        self.text1.delete(1.0,END)
    
    def set_erroinface(self,x,y,erro_type,erro_detail):#设置错误界面
        self.label10.config(text=str(x))
        self.label11.config(text=str(y))
        self.combobox.set(erro_type)
        self.text1.delete(1.0,END)
        self.text1.insert(END,erro_detail)



Main()