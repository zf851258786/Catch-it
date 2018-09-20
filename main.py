# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from Player import Player
from Item import Item
import time
from pylash.utils import stage, init, addChild, KeyCode
from pylash.system import LoadManage
from pylash.display import Sprite, BitmapData, Bitmap, FPS, Animation
from pylash.text import TextField, TextFormatWeight
from pylash.events import MouseEvent, Event, KeyboardEvent
from pylash.ui import LoadingSample1
from pylash.media import Sound

dataList = {}

stageLayer = None
player = None
itemLayer = None
scoreTxt = None
timeTxt = None
addItemSpeed = 40
addItemSpeedIndex = 0
score = 0
keyboardEnabled = False
myTime = 0
beginTime = 0
endTime = 0
lastTime = 0
playerNum = 0
x1 = 0
x2 = 0

class Button(Sprite):
	def __init__(self,image):
		super(Button,self).__init__()
		bmp = Bitmap(BitmapData(image))
		self.addChild(bmp)
def main():
	# 资源列表，列出了所有需要调用的图片资源及路径
	loadList = [
		{"name" : "player0", "path" : "./images/player0.png"},  #游戏角色图片0
		{"name" : "player1", "path" : "./images/player1.png"},  #游戏角色图片1
		{"name" : "player2", "path" : "./images/player2.png"},  #游戏角色图片2
		{"name" : "player3", "path" : "./images/player3.png"},  #游戏角色图片3
		{"name" : "player00", "path" : "./images/player00.png"},  #游戏角色图片00
		{"name" : "player01", "path" : "./images/player01.png"},  #游戏角色图片01
		{"name" : "player02", "path" : "./images/player02.png"},  #游戏角色图片02
		{"name" : "player03", "path" : "./images/player03.png"},  #游戏角色图片03
		{"name" : "bg", "path" : "./images/bg.jpg"},            #游戏背景图片
		{"name" : "bg1", "path" : "./images/bg1.png"},          #规则说明背景图片
		{"name" : "bg2", "path" : "./images/bg2.png"},          #设置界面
		{"name" : "bg3", "path" : "./images/bg3.png"},          #确认设置界面
		{"name" : "item0", "path" : "./images/item0.png"},      #加分物体1
		{"name" : "item1", "path" : "./images/item1.png"},      #加分物体2
		{"name" : "item2", "path" : "./images/item2.png"},      #加分物体3
		{"name" : "item3", "path" : "./images/item3.png"},      #加分物体4
		{"name" : "item4", "path" : "./images/item4.png"},      #减分物体1
		{"name" : "item5", "path" : "./images/item5.png"},      #减分物体2
		{"name" : "item6", "path" : "./images/item6.png"},      #减分物体3
		{"name" : "item7", "path" : "./images/item7.png"},      #减分物体4
		{"name" : "button0", "path" : "./images/button0.png"},  #开始按钮
		{"name" : "button1", "path" : "./images/button1.png"},  #规则介绍按钮
		{"name" : "button2", "path" : "./images/button2.png"},  #返回按钮
		{"name" : "level0", "path" : "./images/level0.png"},    #简单模式
		{"name" : "level1", "path" : "./images/level1.png"},    #中等模式
		{"name" : "level2", "path" : "./images/level2.png"},    #复杂模式
		{"name" : "choice", "path" : "./images/choice.png"},    #选择框
		{"name" : "result0", "path" : "./images/result0.png"},
		{"name" : "result1", "path" : "./images/result1.png"}
	]

	# create loading page
	loadingPage = LoadingSample1()
	#loadingPage是？？？
	#LoadingSample1类在ui.py文件中，是LoadingSample的子类,()中写的是继承的父类,在这里只是标准的类对象生成格式
	addChild(loadingPage)
	#addChild是一个用于把显示对象加到自身这个层上的函数,详见utils.py文件中的全局函数addChild

	def loadComplete(result):
		loadingPage.remove()
		#LoadingSample1类中的父类display.py文件中的DisplayObject类的remove函数，进而使用到了同文件中DisplayObjectContainer类中的removeChild类

		gameInit(result)
		#本文件中的一个全局函数，用于初始化游戏

	# load files
	LoadManage.load(loadList, loadingPage.setProgress, loadComplete)
	#此处为类对象调用，类对象LoadManage调用其类中的load函数，LoadManage类存在于system.py文件中。参数分别为需加载的列表、加载进度显示、加载完成后调用函数存储
	#存在一个问题，result的值是谁传入的？？？

def gameInit(result):
	global dataList, stageLayer     #对全局变量dataList和stageLayer的作用域范围做了扩增

	dataList = result

	# create stage layer
	stageLayer = Sprite()           #创建了一个Sprite类的对象stageLayer
	addChild(stageLayer)            #addChild是一个用于把显示对象加到自身这个层上的函数,详见utils.py文件中的全局函数addChild

	# add FPS                       #这个函数的说明是为了方便查看游戏的效率，还不是很理解？？？
	fps = FPS()
	addChild(fps)

	# add background
	bg = Bitmap(BitmapData(dataList["bg"]))
	#dataList保存加载完成的文件，BitmapData类用于存储图像数据，而Bitmap类用于显示图片,类似于TextField
	stageLayer.addChild(bg)
	#此处使用的不是全局函数addChild,而是stageLayer对象调用的addChild,stageLayer作为self参数传入,使得bd添加在了stageLayer上

	# add some text fields
	titleTxt = TextField()
	titleTxt.text = "忍住不要吃零食"             #游戏的名字
	titleTxt.size = 70
	titleTxt.textColor = "black"
	titleTxt.x = (stage.width - titleTxt.width) / 2    #stage 是一个全局类，用于管理整个窗口，类似于Java中的window
	titleTxt.y = 100
	stageLayer.addChild(titleTxt)
	#TextField类用于显示文本,以上代码生成的是第一行文本，即游戏的名字

	button0 = Button(dataList["button0"])
	button0.x = stage.width - button0.width - 20
	button0.y = 350
	stageLayer.addChild(button0)
	button0.addEventListener(MouseEvent.MOUSE_UP, mySettings)


	button1 = Button(dataList["button1"])
	button1.x = stage.width - button1.width - 20
	button1.y = 420
	stageLayer.addChild(button1)
	button1.addEventListener(MouseEvent.MOUSE_UP, introduction)

	# add event that the game will start when you click
	#stageLayer.addEventListener(MouseEvent.MOUSE_UP, introduction)	
	#stageLayer是一个Sprite类,EventDispatcher是其父类，因此可以直接调用addEventListener,以上代码表示鼠标点击事件，则调用startGame,即开始游戏
	#此处为一个类对象MouseEvent对其成员MOUSE_DOWN的调用
	music0 = Sound()
	music0.load("http:\\bd.kuwo.cn\yinyue\37552330?from=baidu")
	music0.play()
	# add keyboard events to control player
	stage.addEventListener(KeyboardEvent.KEY_DOWN, keyDown)
	stage.addEventListener(KeyboardEvent.KEY_UP, keyUp)
	#加入键盘事件,用于控制游戏中的人物？？？同样为类对象调用
	#keyDown和keyUp都是同文件中定义的函数,keyUp指的是按键未按下的状态,keyDown指的是案件按下的状态


def introduction(e):            #游戏规则介绍
	
	stageLayer.removeAllChildren()
	stageLayer.removeAllEventListeners()
	# add background
	bg1 = Bitmap(BitmapData(dataList["bg1"]))
	stageLayer.addChild(bg1)
	
	button3 = Button(dataList["button0"])
	button3.x = stage.width - button3.width - 10
	button3.y = 520
	stageLayer.addChild(button3)
	button3.addEventListener(MouseEvent.MOUSE_UP, mySettings)

def mySettings(e):                #挑选难度等级以及人物形象
	global playerNum, stageLayer,myTime
	def myplayernum0(e):
		global playerNum, stageLayer,x1
		playerNum = 0
		x1 = 150
	def myplayernum1(e):
		global playerNum, stageLayer,x1
		playerNum = 1
		x1 = 300
	def myplayernum2(e):
		global playerNum, stageLayer,x1
		playerNum = 2
		x1 = 450
	def myplayernum3(e):
		global playerNum, stageLayer,x1
		playerNum = 3
		x1 = 600
	def myspeed0(e):
		global myTime,stageLayer,x2
		Item.mySpeed = 5
		myTime = 30
		x2 = 150
	def myspeed1(e):
		global myTime, stageLayer,x2
		Item.mySpeed = 8
		myTime = 45
		x2 = 300
	def myspeed2(e):
		global myTime, stageLayer,x2
		Item.mySpeed = 10
		myTime = 60
		x2 = 450

	stageLayer.removeAllChildren()
	stageLayer.removeAllEventListeners()

	bg2 = Bitmap(BitmapData(dataList["bg2"]))
	stageLayer.addChild(bg2)

	button00 = Button(dataList["player00"])
	button00.x = 150
	button00.y = 150
	stageLayer.addChild(button00)
	button00.addEventListener(MouseEvent.MOUSE_UP, myplayernum0)

	button01 = Button(dataList["player01"])
	button01.x = 300
	button01.y = 150
	stageLayer.addChild(button01)
	button01.addEventListener(MouseEvent.MOUSE_UP, myplayernum1)
	
	button02 = Button(dataList["player02"])
	button02.x = 450
	button02.y = 150
	stageLayer.addChild(button02)
	button02.addEventListener(MouseEvent.MOUSE_UP, myplayernum2)

	button03 = Button(dataList["player03"])
	button03.x = 600
	button03.y = 150
	stageLayer.addChild(button03)
	button03.addEventListener(MouseEvent.MOUSE_UP, myplayernum3)

	button10 = Button(dataList["level0"])
	button10.x = 175
	button10.y = 350
	stageLayer.addChild(button10)
	button10.addEventListener(MouseEvent.MOUSE_UP, myspeed0)

	button11 = Button(dataList["level1"])
	button11.x = 350
	button11.y = 350
	stageLayer.addChild(button11)
	button11.addEventListener(MouseEvent.MOUSE_UP, myspeed1)
	
	button12 = Button(dataList["level2"])
	button12.x = 525
	button12.y = 350
	stageLayer.addChild(button12)
	button12.addEventListener(MouseEvent.MOUSE_UP, myspeed2)

	button4 = Button(dataList["button0"])
	button4.x = stage.width - button4.width - 10
	button4.y = 520
	stageLayer.addChild(button4)
	button4.addEventListener(MouseEvent.MOUSE_UP, ensureSettings)


def ensureSettings(e):
	global playerNum, stageLayer
	stageLayer.removeAllChildren()
	stageLayer.removeAllEventListeners() 
	bg3 = Bitmap(BitmapData(dataList["bg3"]))
	stageLayer.addChild(bg3)	


	myPlayer = Bitmap(BitmapData(dataList["player0%d"%playerNum]))
	myPlayer.x = (stageLayer.width - myPlayer.width) /2
	myPlayer.y = 150
	stageLayer.addChild(myPlayer)
	
	Myspeed = Bitmap(BitmapData(dataList["level%d"%(x2/150-1)]))
	Myspeed.x = (stageLayer.width - myPlayer.width) / 2 + 17
	Myspeed.y = 350
	stageLayer.addChild(Myspeed)
	
	button0 = Button(dataList["button2"])
	button0.x = 150
	button0.y = 450
	stageLayer.addChild(button0)
	button0.addEventListener(MouseEvent.MOUSE_UP, mySettings)

	button1 = Button(dataList["button0"])
	button1.x = 450
	button1.y = 450
	stageLayer.addChild(button1)
	button1.addEventListener(MouseEvent.MOUSE_UP, startGame)

def startGame(e):
	global player, itemLayer, scoreTxt, addItemSpeedIndex, score, keyboardEnabled,beginTime, timeTxt, playerNum
	# reset some global variables
	addItemSpeedIndex = 0           #掉落物体的时间间隔,即速度
	score = 0                       #玩家分数,可在此处添加数据库用来记录玩家的分数
	beginTime = time.time()
	#初始化一些全局变量

	keyboardEnabled = True
	#用于打开键盘事件,因为键盘事件是加到stage对象上的，所以需要增加一个控制变量

	stageLayer.removeAllChildren()          #清空舞台层
	stageLayer.removeAllEventListeners()    #清空舞台事件
	#清空舞台层,包括背景和所有文字以及监听器

	# add background
	bg = Bitmap(BitmapData(dataList["bg"]))         #重新调用舞台背景图片
	stageLayer.addChild(bg)                         #重新使舞台背景图片显示
	#创建背景
	timeTxt = TextField()
	timeTxt.text = "剩余时间: "
	timeTxt.size = 20
	timeTxt.x = (stage.width - timeTxt.width)-40
	stageLayer.addChild(timeTxt)
	# create player
	print(playerNum)
	player = Player(dataList["player%d"%playerNum])
	#调用玩家图片并初始化玩家类对象,player类是我们自己创建的人物类
	
	player.x = (stage.width - player.width) / 2     #定义玩家的初始水平位置，即画面中央
	player.y = 450                                  #定义玩家的初始垂直位置，即画面底部
	stageLayer.addChild(player)                     #使玩家图片显示
	#创建角色

	# create item layer to contain objects falling from the top
	itemLayer = Sprite()                            #创建一个类Sprite的对象,itemLayer,即掉落的物品
	stageLayer.addChild(itemLayer)                  #使物品的图片显示
	
	# set the hit target to confirm a object which will be checked collision with items
	itemLayer.hitTarget = player                    #将人物对象保存到itemLayer中用于碰撞检测,hitTarget来自于？？？


	# add score text field
	scoreTxt = TextField()                          #生成分数文本的实例对象
	scoreTxt.text = "Score: 0"                      #设置分数文本显示的内容
	scoreTxt.textColor = "black"                      
	scoreTxt.size = 30
	scoreTxt.x = scoreTxt.y = 30
	scoreTxt.weight = TextFormatWeight.BOLDER
	stageLayer.addChild(scoreTxt)
	#创建分数文本

	stageLayer.addEventListener(Event.ENTER_FRAME, loop)
	#加入监听器,onMouseDown和onMouseUp都是同文件中定义的函数,onMouseDown指的是一个鼠标按下的状态,onMouseUp指的是鼠标悬空的状态
	#ENTER_REAME是一个时间轴事件,类似于一个计时器,该事件的监听器每隔一段时间就会呗出发一次,事件触发时间间隔取决于init函数的第一个参数

def keyDown(e):
	global player

	if not keyboardEnabled or not player:
		return

	if e.keyCode == KeyCode.KEY_RIGHT:
		player.direction = "right"
	elif e.keyCode == KeyCode.KEY_LEFT:
		player.direction = "left"
	#按键落下时角色受玩家控制左右移动

def keyUp(e):
	global player

	if not keyboardEnabled or not player:
		return

	player.direction = None
	#按键抬起使角色静止

def loop(e):
	global player, itemLayer, addItemSpeed, addItemSpeedIndex, begintime, endtime,score

	player.loop()

	for o in itemLayer.childList:
		o.loop()
	
	# control the speed of adding a item
	if addItemSpeedIndex < addItemSpeed:
		addItemSpeedIndex += 1

		return

	addItemSpeedIndex = 0
	# get random item
	randomNum = random.randint(0, 7)
	#随机获得落下的物体数量

	# add a item
	item = Item(dataList["item" + str(randomNum)])          #随机选择不同的物体落下
	item.index = randomNum
	item.x = int(random.randint(30, stage.width - 100))
	itemLayer.addChild(item)
	
	if getTime(e) <= 0 or score < 0:                        #结束游戏
		gameOver(e)

	
	item.addEventListener(Item.EVENT_ADD_SCORE, addScore)
	item.addEventListener(Item.EVENT_MINUS_SCORE,minusScore)
	item.addEventListener(Item.EVENT_GAME_OVER, gameOver)

def getTime(e):
	global beginTime,endTime,timeTxt,myTime

	endTime = time.time()

	lastTime = myTime - int(endTime - beginTime)

	timeTxt.text = "剩余时间: %d s"%lastTime

	return lastTime

def addScore(e):
	global score, scoreTxt

	score += 1

	scoreTxt.text = "Score: %s" % score
	
def minusScore(e):
	global score, scoreTxt

	score -= 3

	scoreTxt.text = "Score: %s" % score

def gameOver(e):
	global player, scoreTxt, stageLayer, keyboardEnabled, playernum

	keyboardEnabled = False
	stageLayer.removeAllEventListeners()

	scoreTxt.remove()
	player.animation.stop()

	resultTxt = TextField()
	
	if score < 0:
		resultTxt.text = "你输啦！再试一次吧！"
		result0 = Bitmap(BitmapData(dataList["result0"]))
		result0.x = (stageLayer.width - result0.width) /2
		result0.y = 150
		stageLayer.addChild(result0)

		
	else:
		resultTxt.text = "恭喜胜利！最终得分为: %s" % score
		result1 = Bitmap(BitmapData(dataList["result1"]))
		result1.x = (stageLayer.width - result1.width) /2
		result1.y = 150
		stageLayer.addChild(result1)
	resultTxt.size = 40
	resultTxt.weight = TextFormatWeight.BOLD
	resultTxt.textColor = "black"
	resultTxt.x = (stage.width - resultTxt.width) / 2
	resultTxt.y = 250
	stageLayer.addChild(resultTxt)

	hintTxt = TextField()
	hintTxt.text = "双击鼠标左键再次开始游戏"
	hintTxt.size = 35
	hintTxt.textColor = "black"
	hintTxt.x = (stage.width - hintTxt.width) / 2
	hintTxt.y = 320
	stageLayer.addChild(hintTxt)

	# add double click event to restart
	stageLayer.addEventListener(MouseEvent.DOUBLE_CLICK, startGame)

init(1000 / 60, "Get Fruits", 800, 600, main)
#初始化窗口,参数分别为时间轴事件更新的事件、窗口的名称、窗口的长和宽、主函数的调用

