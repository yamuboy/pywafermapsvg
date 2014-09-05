#!/usr/local/bin/python

class pyWaferMapSVG:
	def __init__(self, elementSize, notchOrient="down", waferSizemm=300.0):
		self.setWaferSpec(elementSize, notchOrient, waferSizemm)
			
	def setWaferSpec(self, elementSize, notchOrient, waferSizemm):
		self.dieX = None
		self.dieY = None
		self.die_coordinates = None
		self.elementSize = float(elementSize)
		self.waferSize = float(waferSizemm)
		self.waferCenter = self.elementSize / 2.0
		self.waferRadius = self.elementSize / 2.0 * 0.9
		notchOrient = notchOrient.lower()
		if notchOrient != "up" and notchOrient != "down" and notchOrient != "right" and notchOrient != "left":
			raise Exception('supported notch orientatoins: down|up|right|left')
		else:
			self.notch = notchOrient
			
	def setDieMaps(self, dieXmm, dieYmm, coordinate_list):
		self.dieX = float(dieXmm)/self.waferSize * self.waferRadius * 2
		self.dieY = float(dieYmm)/self.waferSize * self.waferRadius * 2
		self.die_coordinates = []
		for info in coordinate_list:
			die_info = []
			self.die_coordinates.append(die_info)
			for i,item in enumerate(info):
				if i < 2:
					die_info.append(float(item)/self.waferSize * self.waferRadius * 2 + self.elementSize/2 - self.waferRadius)
				else:
					die_info.append(item)
		
	def drawDies(self, sb):
		for die_info in self.die_coordinates:
			if len(die_info) > 2:
				die_color = die_info[2]
				if len(die_info) > 3:
					msg = die_info[3]
				else:
					msg = ''
			else:
				die_color = 'white'
			sb.append('<rect onmouseenter="mouseEnterEventHandler(evt,\''+msg+'\')" onmouseleave="mouseLeaveEventHandler(evt)" x="'+str(die_info[0])+'" y="'+str(die_info[1])+'" width="'+str(self.dieX)+'" height="'+str(self.dieY)+'" style="fill:'+die_color+';stroke:darkgray;stroke-width:2;fill-opacity:0.7;stroke-opacity:0.9" />')
			
	def drawNotch(self, sb):
		b = 2 * self.waferRadius * 0.034899
		h = b * 0.034899
		d = b * 0.999391
		if self.notch == "up":
			x1 = self.waferCenter - d
			y1 = self.waferCenter - self.waferRadius + h
			x2 = self.waferCenter
			y2 = y1 + 10.0*h
			x3 = self.waferCenter + d
			y3 = y1
		elif self.notch == "left":
			x1 = self.waferCenter - self.waferRadius + h
			y1 = self.waferCenter - d
			x2 = x1 + 10.0*h
			y2 = self.waferCenter
			x3 = x1
			y3 = self.waferCenter + d
		elif self.notch == "right":
			x1 = self.waferCenter + self.waferRadius - h
			y1 = self.waferCenter - d
			x2 = x1 - 10.0*h
			y2 = self.waferCenter
			x3 = x1
			y3 = self.waferCenter + d
		else:
			x1 = self.waferCenter - d
			y1 = self.waferCenter + self.waferRadius - h
			x2 = self.waferCenter
			y2 = y1 - 10.0*h
			x3 = self.waferCenter + d
			y3 = y1
		sb.append('<polyline points="'+str(x1)+','+str(y1)+' '+str(x2)+','+str(y2)+' '+str(x3)+','+str(y3)+'" style="fill:none;stroke:black;stroke-width:1" />')
		
	def makeSVG(self):
		sb = []
		sb.append(
				"""
				<script type="text/javascript">
					function mouseEnterEventHandler(e,msg){
						if(msg.trim() != ''){
							document.getElementById('msgText').innerHTML = msg;
							var tooltip = document.getElementById('waferMapToolTip');
							tooltip.style.left=e.clientX + 30 + "px";
							tooltip.style.top=e.clientY + "px";
							tooltip.style.display='block';
						}
					}
					function mouseLeaveEventHandler(e){
						document.getElementById('waferMapToolTip').style.display='none';
					}
				</script>
				""")
		sb.append('<div id="waferMapToolTip" style="background-color:#FFCC66;opacity:0.8;border-radius:8px;display:none;position:absolute;"><div id="msgText" style="margin:5px;">hello!</div></div>')
		sb.append('<svg height="'+str(self.elementSize)+'" width="'+str(self.elementSize)+'">')
		sb.append('<circle cx="'+str(self.waferCenter)+'" cy="'+str(self.waferCenter)+'" r="'+str(self.waferRadius)+'" stroke="black" stroke-width="1" fill="none" />')
		self.drawNotch(sb)
		if self.dieX != None and self.dieY != None and self.die_coordinates != None:
			self.drawDies(sb)
		sb.append('</svg>')
		return ''.join(sb)