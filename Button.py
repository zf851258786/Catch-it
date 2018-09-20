from pylash.display import Sprite, BitmapData, Bitmap

class Button(Sprite):
	def __init__(self,image,X,Y):
		super(Button,self).__init__()
		bmp = Bitmap(BitmapData(image))
		self.addChild(bmp)		
		self.x = X
		self.y = Y
