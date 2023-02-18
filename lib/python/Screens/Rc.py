from Components.Pixmap import MovingPixmap, MultiPixmap
from Tools.Directories import resolveFilename, SCOPE_SKIN
from xml.etree.ElementTree import ElementTree
from Components.config import config, ConfigInteger
from Tools.HardwareInfo import HardwareInfo
import skin

config.misc.rcused = ConfigInteger(default = 1)

class Rc:
	def __init__(self):
		self["rc"] = MultiPixmap()
		self["arrowdown"] = MovingPixmap()
		self["arrowdown2"] = MovingPixmap()
		self["arrowup"] = MovingPixmap()
		self["arrowup2"] = MovingPixmap()

		self.initRcused()

		(rcArrowDownW, rcArrowDownH, rcArrowUpW, rcArrowUpH, rcheight, rcheighthalf) = (18, 70, 18, 0, 500, 250)
		if config.misc.rcused == 2:
			(rcArrowDownW, rcArrowDownH, rcArrowUpW, rcArrowUpH, rcheight, rcheighthalf) = skin.parameters.get("RcArrow", (18, 70, 18, 0, 500, 250))

		self.rcheight = rcheight
		self.rcheighthalf = rcheighthalf
		
		self.selectpics = []
		self.selectpics.append((self.rcheighthalf, ["arrowdown", "arrowdown2"], (-rcArrowDownW, -rcArrowDownH)))
		self.selectpics.append((self.rcheight, ["arrowup", "arrowup2"], (-rcArrowUpW, rcArrowUpH)))
		
		self.readPositions()
		self.clearSelectedKeys()
		self.onShown.append(self.initRc)

	def initRcused(self):
		if config.misc.firstrun.value:
			boxType = HardwareInfo().get_vu_device_name()

			if boxType in ('bm750', 'uno', 'ultimo', 'solo2', 'duo2', 'solose', 'zero', 'solo4k', 'uno4k', 'ultimo4k'):
				config.misc.rcused.value = 0
			elif boxType == 'solo':
				config.misc.rcused.value = 1
			else:
				config.misc.rcused.value = 2
			config.misc.rcused.save()

	def initRc(self):
		self["rc"].setPixmapNum(config.misc.rcused.value)		
				
	def readPositions(self):
		tree = ElementTree(file = resolveFilename(SCOPE_SKIN, "rcpositions.xml"))
		rcs = tree.getroot()
		self.rcs = {}
		for rc in rcs:
			id = int(rc.attrib["id"])
			self.rcs[id] = {}
			for key in rc:
				name = key.attrib["name"]
				pos = key.attrib["pos"].split(",")
				self.rcs[id][name] = (int(pos[0]), int(pos[1]))
		
	def getSelectPic(self, pos):
		for selectPic in self.selectpics:
			if pos[1] <= selectPic[0]:
				return (selectPic[1], selectPic[2])
		return None
	
	def hideRc(self):
		self["rc"].hide()
		self.hideSelectPics()
		
	def showRc(self):
		self["rc"].show()

	def selectKey(self, key):
		rc = self.rcs[config.misc.rcused.value]
		if rc.has_key(key):
			rcpos = self["rc"].getPosition()
			pos = rc[key]
			selectPics = self.getSelectPic(pos)
			selectPic = None
			for x in selectPics[0]:
				if x not in self.selectedKeys:
					selectPic = x
					break
			if selectPic is not None:
				print "selectPic:", selectPic
				self[selectPic].moveTo(rcpos[0] + pos[0] + selectPics[1][0], rcpos[1] + pos[1] + selectPics[1][1], 1)
				self[selectPic].startMoving()
				self[selectPic].show()
				self.selectedKeys.append(selectPic)
	
	def clearSelectedKeys(self):
		self.showRc()
		self.selectedKeys = []
		self.hideSelectPics()
		
	def hideSelectPics(self):
		for selectPic in self.selectpics:
			for pic in selectPic[1]:
				self[pic].hide()
