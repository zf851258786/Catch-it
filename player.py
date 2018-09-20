from pylash.utils import stage
from pylash.display import Sprite, Animation, BitmapData

#定义了人物类
class Player(Sprite):
	def __init__(self, playerImage):
		super(Player, self).__init__()

                #移动方向[right向右，left向左，None不移动]
		self.direction = None
		#移动速度
		self.step = 5
		
		# create bitmap data
		bmpd = BitmapData(playerImage)
                #创建图片数据

		# create frames in animation
		frames = Animation.divideUniformSizeFrames(bmpd.width, bmpd.height, 4, 4)
                #创建动画帧列表，通过类对象Animation调用divideUniformSizeFrames函数

		# create animation
		self.animation = Animation(bmpd, frames)                #创建动画
		self.animation.speed = 5                                #设置动画播放速度
		self.animation.play()                                   #播放动画
		self.addChild(self.animation)                           #将动画加入界面
		#创建动画

	def loop(self):
		# move towards right
		if self.direction == "right":
			self.x += self.step
			self.animation.currentRow = 2
		# move towards left
		elif self.direction == "left":
			self.x -= self.step
			self.animation.currentRow = 1
		# no movement
		else:
			self.animation.currentRow = 0

		if self.x < 0:
			self.x = 0

		elif self.x > stage.width - self.width:
			self.x = stage.width - self.width



