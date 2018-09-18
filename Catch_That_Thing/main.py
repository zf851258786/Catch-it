# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from Player import Player
from Item import Item

from pylash.utils import stage, init, addChild, KeyCode
from pylash.system import LoadManage
from pylash.display import Sprite, BitmapData, Bitmap, FPS
from pylash.text import TextField, TextFormatWeight
from pylash.events import MouseEvent, Event, KeyboardEvent
from pylash.ui import LoadingSample1

dataList = {}

stageLayer = None
player = None
itemLayer = None
scoreTxt = None
addItemSpeed = 40
addItemSpeedIndex = 0
score = 0
keyboardEnabled = False

def main():
	# 资源列表，列出了所有需要调用的图片资源及路径
	loadList = [
		{"name" : "player", "path" : "./images/player.png"},    #游戏角色图片
		{"name" : "bg", "path" : "./images/bg.jpg"},            #游戏背景图片
		{"name" : "item0", "path" : "./images/item0.png"},      #加分物体1
		{"name" : "item1", "path" : "./images/item1.png"},      #加分物体2
		{"name" : "item2", "path" : "./images/item2.png"},      #加分物体3
		{"name" : "item3", "path" : "./images/item3.png"},      #加分物体4
		{"name" : "item4", "path" : "./images/item4.png"},      #减分物体1
		{"name" : "item5", "path" : "./images/item5.png"},      #减分物体2
		{"name" : "item6", "path" : "./images/item6.png"},      #减分物体3
		{"name" : "item7", "path" : "./images/item7.png"}       #减分物体4
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
	titleTxt.text = "Get Furit"             #游戏的名字
	titleTxt.size = 70
	titleTxt.textColor = "red"
	titleTxt.x = (stage.width - titleTxt.width) / 2    #stage 是一个全局类，用于管理整个窗口，类似于Java中的window
	titleTxt.y = 100
	stageLayer.addChild(titleTxt)
	#TextField类用于显示文本,以上代码生成的是第一行文本，即游戏的名字

	hintTxt = TextField()
	hintTxt.text = "Tap to Start the Game!~"        #游戏的开始提示
	hintTxt.textColor = "red"
	hintTxt.size = 40
	hintTxt.x = (stage.width - hintTxt.width) / 2
	hintTxt.y = 300
	stageLayer.addChild(hintTxt)
	#以上代码生成的是第二行文本，即提示开始

	engineTxt = TextField()
	engineTxt.text = "- Powered by Pylash -"        #开发人员
	engineTxt.textColor = "red"
	engineTxt.size = 20
	engineTxt.weight = TextFormatWeight.BOLD
	engineTxt.italic = True
	engineTxt.x = (stage.width - engineTxt.width) / 2
	engineTxt.y = 500
	stageLayer.addChild(engineTxt)
	#以上代码生成的是第三行文本，即开发人员名

	# add event that the game will start when you click
	stageLayer.addEventListener(MouseEvent.MOUSE_UP, startGame)
	#stageLayer是一个Sprite类,EventDispatcher是其父类，因此可以直接调用addEventListener,以上代码表示鼠标点击事件，则调用startGame,即开始游戏
        #此处为一个类对象MouseEvent对其成员MOUSE_DOWN的调用

        
	# add keyboard events to control player
	stage.addEventListener(KeyboardEvent.KEY_DOWN, keyDown)
	stage.addEventListener(KeyboardEvent.KEY_UP, keyUp)
	#加入键盘事件,用于控制游戏中的人物？？？同样为类对象调用
        #keyDown和keyUp都是同文件中定义的函数,keyUp指的是按键未按下的状态,keyDown指的是案件按下的状态

def startGame(e):
	global player, itemLayer, scoreTxt, addItemSpeedIndex, score, keyboardEnabled

	# reset some global variables
	addItemSpeedIndex = 0           #掉落物体的时间间隔,即速度
	score = 0                       #玩家分数,可在此处添加数据库用来记录玩家的分数
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

	# create player
	player = Player(dataList["player"])
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
	scoreTxt.textColor = "red"                      
	scoreTxt.size = 30
	scoreTxt.x = scoreTxt.y = 30
	scoreTxt.weight = TextFormatWeight.BOLDER
	stageLayer.addChild(scoreTxt)
	#创建分数文本

	# add events
	#stageLayer.addEventListener(MouseEvent.MOUSE_DOWN, onMouseDown)
	#stageLayer.addEventListener(MouseEvent.MOUSE_UP, onMouseUp)
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

def onMouseDown(e):
	global player
	
	if e.offsetX > (stage.width / 2):
		player.direction = "right"
	else:
		player.direction = "left"
	#鼠标一个按键按下时角色受玩家控制左右移动

def onMouseUp(e):
	global player

	player.direction = None
	#鼠标抬起时角色静止

def loop(e):
	global player, itemLayer, addItemSpeed, addItemSpeedIndex

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
	# add ourselves events
	item.addEventListener(Item.EVENT_ADD_SCORE, addScore)
	item.addEventListener(Item.EVENT_GAME_OVER, gameOver)

def addScore(e):
	global score, scoreTxt

	score += 1

	scoreTxt.text = "Score: %s" % score

def gameOver(e):
	global player, scoreTxt, stageLayer, keyboardEnabled

	keyboardEnabled = False

	stageLayer.removeAllEventListeners()

	scoreTxt.remove()
	player.animation.stop()

	resultTxt = TextField()
	resultTxt.text = "Final Score: %s" % score
	resultTxt.size = 40
	resultTxt.weight = TextFormatWeight.BOLD
	resultTxt.textColor = "orangered"
	resultTxt.x = (stage.width - resultTxt.width) / 2
	resultTxt.y = 250
	stageLayer.addChild(resultTxt)

	hintTxt = TextField()
	hintTxt.text = "Double Click to Restart"
	hintTxt.size = 35
	hintTxt.textColor = "red"
	hintTxt.x = (stage.width - hintTxt.width) / 2
	hintTxt.y = 320
	stageLayer.addChild(hintTxt)

	# add double click event to restart
	stageLayer.addEventListener(MouseEvent.DOUBLE_CLICK, startGame)

init(1000 / 60, "Get Fruits", 800, 600, main)
#初始化窗口,参数分别为时间轴事件更新的事件、窗口的名称、窗口的长和宽、主函数的调用

