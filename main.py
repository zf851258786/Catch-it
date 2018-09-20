# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
from Player import Player
from Item import Item
from Button import Button
from pylash.utils import stage, init, addChild, KeyCode
from pylash.system import LoadManage
from pylash.display import Sprite, BitmapData, Bitmap, FPS, Animation
from pylash.text import TextField, TextFormatWeight
from pylash.events import MouseEvent, Event, KeyboardEvent
from pylash.ui import LoadingSample1
from pylash.media import Sound

dataList = {}                   #用于存储加载完成的资源
stageLayer = None               #界面层
player = None                   #游戏人物
itemLayer = None                #掉落的物品
scoreTxt = None                 #分数对象
timeTxt = None                  #时间对象
keyboardEnabled = False         #键盘使能
addItemSpeed = 40               #物体增加的理想速度
addItemSpeedIndex = 0           #物体增加的实际速度
score = 0                       #分数文本
myTime = 30                     #玩家选择的时间长度
beginTime = 0                   #游戏开始的时间
endTime = 0                     #实时的时间
lastTime = 0                    #剩余时间
playerNum = 0                   #选择的游戏人物序号
Item.mySpeed = 5                #选择的物体掉落速度


def main():

	# 资源列表，列出了所有需要调用的图片资源及路径

	loadList = [
		{"name" : "player0", "path" : "./images/player0.png"},          #游戏角色图片0
		{"name" : "player1", "path" : "./images/player1.png"},          #游戏角色图片1
		{"name" : "player2", "path" : "./images/player2.png"},          #游戏角色图片2
		{"name" : "player3", "path" : "./images/player3.png"},          #游戏角色图片3
		{"name" : "player00", "path" : "./images/player00.png"},        #游戏角色图片00
		{"name" : "player01", "path" : "./images/player01.png"},        #游戏角色图片01
		{"name" : "player02", "path" : "./images/player02.png"},        #游戏角色图片02
		{"name" : "player03", "path" : "./images/player03.png"},        #游戏角色图片03
		{"name" : "bg", "path" : "./images/bg.jpg"},                    #游戏背景图片
		{"name" : "bg1", "path" : "./images/bg1.png"},                  #规则说明背景图片
		{"name" : "bg2", "path" : "./images/bg2.png"},                  #设置界面
		{"name" : "bg3", "path" : "./images/bg3.png"},                  #确认设置界面
		{"name" : "item0", "path" : "./images/item0.png"},              #加分物体1
		{"name" : "item1", "path" : "./images/item1.png"},              #加分物体2
		{"name" : "item2", "path" : "./images/item2.png"},              #加分物体3
		{"name" : "item3", "path" : "./images/item3.png"},              #加分物体4
		{"name" : "item4", "path" : "./images/item4.png"},              #减分物体1
		{"name" : "item5", "path" : "./images/item5.png"},              #减分物体2
		{"name" : "item6", "path" : "./images/item6.png"},              #减分物体3
		{"name" : "item7", "path" : "./images/item7.png"},              #减分物体4
		{"name" : "button0", "path" : "./images/button0.png"},          #开始按钮
		{"name" : "button1", "path" : "./images/button1.png"},          #规则介绍按钮
		{"name" : "button2", "path" : "./images/button2.png"},          #返回按钮
		{"name" : "level0", "path" : "./images/level0.png"},            #简单模式
		{"name" : "level1", "path" : "./images/level1.png"},            #中等模式
		{"name" : "level2", "path" : "./images/level2.png"},            #复杂模式
		{"name" : "choice", "path" : "./images/choice.png"},            #选择框
		{"name" : "result0", "path" : "./images/result0.png"},          #失败装饰品
		{"name" : "result1", "path" : "./images/result1.png"}           #胜利装饰品
		]
	# 加载页
	loadingPage = LoadingSample1()
	#LoadingSample1类在ui.py文件中，是LoadingSample的子类,()中写的是继承的父类,在这里只是标准的类对象生成格式
	addChild(loadingPage)
	#addChild是一个用于把显示对象加到自身这个层上的函数,详见utils.py文件中的全局函数addChild

	def loadComplete(result):
		loadingPage.remove() #把loading页面删除
		#LoadingSample1类中的父类display.py文件中的DisplayObject类的remove函数，进而使用到了同文件中DisplayObjectContainer类中的removeChild类

		gameInit(result) #游戏界面初始化
		#本文件中的一个全局函数，用于初始化游戏

	# 加载文件的命令，实现
	LoadManage.load(loadList, loadingPage.setProgress, loadComplete)
	# 此处为类对象调用，类对象LoadManage调用其类中的load函数，LoadManage类存在于system.py文件中。参数分别为需加载的列表、加载进度显示、加载完成后调用函数存储
	# result的值是由loadList传入的
	# 通过判断loading的进程来判断何时调用loadComplete


# 创建背景的函数
def creatBg(name):
	global dataList,stageLayer
	stageLayer.removeAllChildren()	                # 移除原界面的背景和元素
	stageLayer.removeAllEventListeners()

	# 创建背景元素
	bg = Bitmap(BitmapData(dataList[name]))
	stageLayer.addChild(bg)
	return bg

	
# 创建文本的函数
def creatTxt(Txt,Size,X,Y,Color):
	global stageLayer
	txt = TextField()
	txt.text = Txt
	txt.size = Size
	txt.x = X
	txt.y = Y
	txt.color = Color
	stageLayer.addChild(txt)
	return txt
	# stage 是一个全局类，用于管理整个窗口，类似于Java中的window
	# TextField类用于显示文本

# 创建图片的函数
def creatPict(Name,X,Y):
	global dataList,stageLayer
	picture = Bitmap(BitmapData(dataList[Name]))
	picture.x = X
	picture.y = Y
	stageLayer.addChild(picture)
	return picture

# 创建Button的函数
def creatButton(name,X,Y,function):
	global dataList,stageLayer
	button = Button(dataList[name],X,Y)
	stageLayer.addChild(button)
	button.addEventListener(MouseEvent.MOUSE_UP, function)
	return button
	# button类定义在button.py文件中，是Sprie类的子类
	#此处为一个类对象MouseEvent对其成员MOUSE_DOWN的调用


# 游戏初始界面
def gameInit(result):
	
	global dataList, stageLayer     # 全局变量dataList和stageLayer

	dataList = result               # 将result的值赋给dataList，又因为dataList是全局变量，所以在其他函数中也可以通过dataList调用加载完成的文件

	# 创建主界面
	stageLayer = Sprite()           # 创建了一个Sprite类的对象stageLayer
	addChild(stageLayer)            # addChild是一个用于把显示对象加到自身这个层上的函数,详见utils.py文件中的全局函数addChild

	# 创建背景元素
	bg = Bitmap(BitmapData(dataList["bg"]))
	#dataList保存加载完成的文件，BitmapData类用于存储图像数据，而Bitmap类用于显示图片,类似于TextField
	stageLayer.addChild(bg)
	#此处使用的不是全局函数addChild,而是stageLayer对象调用的addChild,stageLayer作为self参数传入,使得bd添加在了stageLayer上

	# 创建文本元素
	titleTxt = creatTxt("忍住不能吃零食",70,155,100,"black")                        #以上代码生成的是第一行文本，即游戏的名字

	# 创建按钮元素
	button0 = creatButton("button0",stage.width - 225,350, mySettings)              # button0是"开始游戏"按钮，点击按钮进入"设置"界面
	button1 = creatButton("button1",stage.width - 225,420, introduction)            # button1是"规则介绍"按钮，点击按钮进入"规则介绍"界面

	# 创建音乐播放元素	
	music0 = Sound()
	music0.load("http:\\bd.kuwo.cn\yinyue\37552330?from=baidu")
	music0.play()
	#未能正常运行
	
	# 添加监听器
	stage.addEventListener(KeyboardEvent.KEY_DOWN, keyDown)
	stage.addEventListener(KeyboardEvent.KEY_UP, keyUp)
	#加入键盘事件,用于控制游戏人物，同样为类对象调用
	#keyDown和keyUp都是同文件中定义的函数,keyUp指的是按键未按下的状态,keyDown指的是案件按下的状态


# 规则介绍界面
def introduction(e):
        
	# 创建背景元素
	bg = creatBg("bg1")

	# 创建按钮元素
	button3 = creatButton("button0",stage.width - 215,520,mySettings)               # button3是"开始游戏"按钮，点击按钮进入"设置"界面


# 设置界面(人物形象及难度等级)
def mySettings(e):
	
	global stageLayer               # 全局变量stageLayer

	# 选中第一个游戏人物角色
	def myplayernum0(e):
		global playerNum        # 全局变量playerNum
		playerNum = 0           # 选中的游戏人物序号设置为0
	# 选中第二个游戏人物角色
	def myplayernum1(e):
		global playerNum
		playerNum = 1
	# 选中第三个游戏人物角色
	def myplayernum2(e):
		global playerNum
		playerNum = 2
	# 选中第四个游戏人物角色
	def myplayernum3(e):
		global playerNum
		playerNum = 3

	# 选中第一个难度等级(易)
	def myspeed0(e):
		global myTime           # 全局变量myTime
		Item.mySpeed = 5        # 物体下落速度设置为5
		myTime = 30             # 倒计时设置为30s
	# 选中第二个难度等级(中)
	def myspeed1(e):
		global myTime
		Item.mySpeed = 8
		myTime = 45
	# 选中第三个难度等级(难)
	def myspeed2(e):
		global myTime
		Item.mySpeed = 10
		myTime = 60

        # 创建背景元素
	bg = creatBg("bg2")

	# 创建按钮元素
	button00 = creatButton("player00",150,150,myplayernum0)                         # button00是第一个游戏人物按钮，点击按钮进入myplaernum0函数，即把选中的游戏人物序号设置为0
	button01 = creatButton("player01",300,150,myplayernum1)
	button02 = creatButton("player02",450,150,myplayernum2)
	button03 = creatButton("player03",600,150,myplayernum3)
	button10 = creatButton("level0",175,350,myspeed0)                               # button10是第一个难度等级按钮，点击按钮进入myspeed0函数，即把物体下落速度设置为5，倒计时设置为30s
	button11 = creatButton("level1",350,350,myspeed1)                               
	button12 = creatButton("level2",525,350,myspeed2)
	button4 = creatButton("button0",stage.width-215,520,ensureSettings)             # button4是"开始游戏"按钮


# 确定设置界面
def ensureSettings(e):

	global playerNum, stageLayer                                                    # 全局变量playerNum，stageLayer

        # 创建背景元素
	bg = creatBg("bg3")

	# 创建图片元素
	myPlayer = creatPict("player0%d"%playerNum,354.5,150)                           # 我选择的游戏人物的图片
	Myspeed = creatPict("level%d"%(myTime/15-2),371.5,350)                          # 我选择的难度等级的图片

	# 创建按钮元素
	button0 = creatButton("button2",150,450,mySettings)                             # button0是'返回'按钮
	button1 = creatButton("button0",450,450,startGame)                              # button1是'开始游戏'按钮


# 游戏界面
def startGame(e):

	global player, itemLayer, scoreTxt, addItemSpeedIndex, score, keyboardEnabled,beginTime, timeTxt, playerNum

	# 重新设置全局变量的值
	addItemSpeedIndex = 0                                                           # 添加掉落物体的速度
	score = 0                                                                       # 玩家分数,可在此处添加数据库用来记录玩家的分数！！！！！！！！！！！
	beginTime = time.time()                                                         # 设置游戏开始时间
	keyboardEnabled = True                                                          # 设置键盘事件使能
	#用于打开键盘事件,因为键盘事件是加到stage对象上的，stage生成后就可以通过键盘控制，不是我们想要的结果，所以需要增加一个控制变量

        # 创建背景元素
	bg = creatBg("bg")

	# 创建文本元素
	timeTxt = creatTxt("剩余时间: ",20,668,0,'black')                               # 文本内容是游戏的剩余时间
	
	# 创建人物元素
	player = Player(dataList["player%d"%playerNum])                                 # 调用选择的人物图片，创建人物类的实例对象
	player.x = (stage.width - player.width) / 2                                     # 设置人物元素初始水平位置
	player.y = 450                                                                  # 设置人物元素初始垂直位置
	stageLayer.addChild(player)                                                     # 使人物元素图片显示在游戏界面上

	# 创建物体元素
	itemLayer = Sprite()                                                            # 创建物体层
	stageLayer.addChild(itemLayer)                                                  # 使物体层显示在游戏界面上
	
	# 检测与物体元素接触的元素
	itemLayer.hitTarget = player                                                    # 将需要检测的元素设置为人物类元素

	# 添加文本元素
	scoreTxt = creatTxt("Score: 0",30,30,30,"black")                                # 文本内容为实时的分数
	scoreTxt.weight = TextFormatWeight.BOLDER                                       

	# 添加监听器
	stageLayer.addEventListener(Event.ENTER_FRAME, loop)
	# ENTER_REAME是一个时间轴事件,类似于一个计时器,该事件的监听器每隔一段时间就会被触发一次,事件触发时间间隔取决于init函数的第一个参数


# 按键按下状态的函数
def keyDown(e):
	
	global player

	if not keyboardEnabled or not player:                                           # 检测键盘事件使能是否开启或与物体产生碰撞的不是人物元素
		return

	if e.keyCode == KeyCode.KEY_RIGHT:                                              # 检测键盘向右方向键是否被按下，若为真，则将人物移动方向设置为向右
		player.direction = "right"
	elif e.keyCode == KeyCode.KEY_LEFT:                                             # 检测键盘向左方向键是否被按下，若为真，则将人物移动方向设置为向左
		player.direction = "left"
	#按键落下时角色受玩家控制左右移动


# 按键抬起状态的函数
def keyUp(e):
	
	global player

	if not keyboardEnabled or not player:
		return

	player.direction = None                         # 将人物设置为静止
	#按键抬起使角色静止


# 剩余时间计算函数
def getTime(e):
	
	global beginTime,endTime,timeTxt,myTime

	endTime = time.time()                           # 调用此时的时间

	lastTime = myTime - int(endTime - beginTime)    # 计算剩余的时间

	timeTxt.text = "剩余时间: %d s"%lastTime        # 设置时间文本的内容

	return lastTime                                 # 返回剩余时间


# 加分函数
def addScore(e):
	
	global score, scoreTxt

	score += 1

	scoreTxt.text = "Score: %s" % score             # 设置分数文本的内容


# 减分函数	
def minusScore(e):
	
	global score, scoreTxt

	score -= 3

	scoreTxt.text = "Score: %s" % score             # 设置分数文本的内容


# 循环执行函数
def loop(e):
	
	global player, itemLayer, addItemSpeed, addItemSpeedIndex, begintime, endtime,score

	player.loop()                                                   # 调用人物元素的循环函数

	for o in itemLayer.childList:                                   # 依次调用各种类型的物体元素的循环函数
		o.loop()
		
	if addItemSpeedIndex < addItemSpeed:                            # 控制物体增加的速度，使其接近理想速度
		addItemSpeedIndex += 1
		return

	addItemSpeedIndex = 0
	
	randomNum = random.randint(0, 7)                                # 随机获得落下的物体元素的序号

	# 创建物体元素
	item = Item(dataList["item" + str(randomNum)])                  # 创建物体类的实例对象，为上一行中获得的序号对应元素
	item.index = randomNum
	item.x = int(random.randint(30, stage.width - 100))             # 设置物体元素的水平位置
	itemLayer.addChild(item)                                        # 使物体元素显示到物体层上
	
	if getTime(e) <= 0 or score < 0:                                # 判断游戏结束条件(剩余时间<=0或实时得分<0)
		gameOver(e)                                             # 调用游戏结束函数

	# 添加监视器
	item.addEventListener(Item.EVENT_ADD_SCORE, addScore)           # 监视"加分物体碰到人物"的事件，调用加分函数
	item.addEventListener(Item.EVENT_MINUS_SCORE,minusScore)        # 监视"减分物体碰到人物"的事件，调用减分函数


# 游戏结束
def gameOver(e):
	
	global player, scoreTxt, stageLayer, keyboardEnabled, playernum

	keyboardEnabled = False                                         # 键盘事件使能关闭
	
	stageLayer.removeAllEventListeners()                            # 删除所有监听器
	scoreTxt.remove()                                               # 删除分数文本元素
	player.animation.stop()                                         # 删除人物元素动画

	# 创建文本元素
	if score < 0:                                                   # 如果得分为负，则失败
		txt = "你输啦！再试一次吧！"                            # 设置"失败"的文本内容
		temp_x = 360
		temp_y = 150
		resultPict_num = 0	                                # 设置游戏失败的图片
	else:
		txt = "恭喜胜利！最终得分为: %s" % score                # 如果得分为正，则成功
		temp_x = -13
		temp_y = 50
		resultPict_num = 1                                      # 设置游戏胜利的图片
	resultTxt = creatTxt(txt,40,195,250,"black")                    # 结束时显示的文本
	
	# 创建图片元素
	resultPict = creatPict("result%d"%resultPict_num,temp_x,temp_y) # 结束时的装饰图片

	# 创建文本元素
	hintTxt = creatTxt("双击鼠标左键再次开始游戏",35,190,320,"black")# 提示双击页面重新开始游戏

	# 添加监听器
	stageLayer.addEventListener(MouseEvent.DOUBLE_CLICK, startGame)  # 用于监听"鼠标点击"事件，开始游戏

# 初始化函数
init(1000 / 60, "别偷吃零食", 800, 600, main)
#初始化窗口,参数分别为时间轴事件更新的速度、窗口的名称、窗口的长和宽、主函数的调用
# 文件的入口



