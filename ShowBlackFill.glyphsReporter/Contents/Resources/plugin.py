# encoding: utf-8

from GlyphsApp.plugins import *
from GlyphsApp import *

class ShowBlackFill(ReporterPlugin):

	def settings(self):
		self.menuName = Glyphs.localize({'en': u'Black Fill'})
#		self.generalContextMenus = [ {'name': Glyphs.localize({'en': u'Disable Nodes and Handles'}), 'action': self.disableNodesHandles} ]

	def getNodesInfo( self, thisLayer ):  #Returns a list of all On-curve nodes.
		try:
			unselectedNodes = []
			selectedSmooths = []
			selectedSharps = []
			selectedOffCurves = []
			for thisPath in thisLayer.paths:
				unselectedNodes += [node for node in thisPath.nodes if not node in thisLayer.selection]
			if thisLayer.selection:
				for n in thisLayer.selection:
					if type(n) == GSNode:
						if n == n.parent.nodes[0] or n == n.parent.nodes[-1]:
							if n.parent.closed is False:
								selectedSharps.append(n)
						if n.type != GSOFFCURVE and n.connection == GSSMOOTH:
							selectedSmooths.append(n)
						elif n.type != GSOFFCURVE and n.connection == GSSHARP:
							selectedSharps.append(n)
						elif n.type == GSOFFCURVE:
							selectedOffCurves.append(n)
			masterList = [unselectedNodes, selectedSmooths, selectedSharps, selectedOffCurves]
			return masterList
		except Exception, e:
			return [[],[],[],[]]
			Glyphs.showMacroWindow()
			print "Show Black Fill error (getNodesInfo): %s" % e

	def getHandlesInfo( self, thisLayer ): # Returns a list of Handles that need to be outlined.
		try:
			returnList = []
			currentSelection = thisLayer.selection
			for thisPath in thisLayer.paths:
				thisPathLength = len( thisPath.nodes )
				for i in range( len( thisPath.nodes )):
					thisNode = thisPath.nodes[ i ]
					if thisNode in currentSelection:
						prevNode = thisPath.nodes[ (i-1) % thisPathLength]
						nextNode = thisPath.nodes[ (i+1) % thisPathLength]
						if thisNode.type == GSOFFCURVE:
							if prevNode.type != GSOFFCURVE:
								returnList.append( (prevNode, thisNode) )
								if not nextNode in currentSelection:
									returnList.append( ( thisPath.nodes[ (i+2) % thisPathLength], nextNode ) )
							elif nextNode.type != GSOFFCURVE:
								returnList.append( (nextNode, thisNode) )
								if not prevNode in currentSelection:
									returnList.append( ( thisPath.nodes[ (i-2) % thisPathLength], prevNode ) )
						else:
							if prevNode.type == GSOFFCURVE and not prevNode in currentSelection:
								returnList.append( (thisNode, prevNode) )
								prevPrevNode = thisPath.nodes[ (i-2) ]
								prevPrevPrevNode = thisPath.nodes[ (i-3) ]
								if prevPrevNode not in currentSelection and prevPrevPrevNode not in currentSelection:
									returnList.append( (prevPrevPrevNode, prevPrevNode) )
							if nextNode.type == GSOFFCURVE and not nextNode in currentSelection:
								returnList.append( (thisNode, nextNode) )
								nextNextNode = thisPath.nodes[ (i+2) % thisPathLength ]
								nextNextNextNode = thisPath.nodes[ (i+3) % thisPathLength ]
								if nextNextNode not in currentSelection and nextNextNextNode not in currentSelection:
									returnList.append( (nextNextNextNode, nextNextNode) )
			return list(set(returnList))
		except Exception, e:
			Glyphs.showMacroWindow()
			print "Show Black Fill error (getHandlesInfo): %s" % e

	def roundDotForPoint( self, thisPoint, markerWidth ): # Returns a circle with thisRadius around thisPoint.
		try:
			myRect = NSRect( ( thisPoint.x - markerWidth * 0.5, thisPoint.y - markerWidth * 0.5 ), ( markerWidth, markerWidth ) )
			return NSBezierPath.bezierPathWithOvalInRect_(myRect)
		except Exception, e:
			Glyphs.showMacroWindow()
			print "Show Black Fill error (roundDotForPoint): %s" % e

	def squareDotForPoint( self, thisPoint, markerWidth ): # Returns a square with thisRadius around thisPoint.
		try:
			myRect = NSRect( ( thisPoint.x - markerWidth * 0.5, thisPoint.y - markerWidth * 0.5 ), ( markerWidth, markerWidth ) )
			return NSBezierPath.bezierPathWithRect_(myRect)
		except Exception, e:
			Glyphs.showMacroWindow()
			print "Show Black Fill error (squareDotForPoint): %s" % e

	def foreground(self, layer):
		try:
			nodesLists = self.getNodesInfo( layer )
		except:
			pass
		try: # outlines
			NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.0, 0.0, 0.0, 0.85 ).set()
			if layer.bezierPath:
				layer.bezierPath.fill()
		except Exception, e:
			Glyphs.showMacroWindow()
			print "Show Black Fill error (foreground): %s" % e
		try: # components
			NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.0, 0.0, 0.0, 0.7 ).set()	
			if layer.components:
				for c in layer.components:
					c.bezierPath.fill()
					#self.bezierPathComp(layer).fill()
		except Exception, e:
			Glyphs.showMacroWindow()
			print "Show Black Fill error (foreground): %s" % e
		try: # nodes
			HandleSize = self.getHandleSize()
			scale = self.getScale()
			zoomedHandleSize = HandleSize / scale
			handleStroke = 1.0 / scale

			# Selected handles lined
			NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.5, 0.5, 0.5, 0.5).set()
			circlesToBeDrawn = NSBezierPath.alloc().init()
			linesToBeDrawn   = NSBezierPath.alloc().init()
			for thisPointPair in self.getHandlesInfo( layer ):
				fromPoint = thisPointPair[0]
				toPoint   = thisPointPair[1]
				linesToBeDrawn.moveToPoint_( NSPoint(fromPoint.x, fromPoint.y) )
				linesToBeDrawn.lineToPoint_( NSPoint(toPoint.x, toPoint.y) )
				circlesToBeDrawn.appendBezierPath_( self.roundDotForPoint( toPoint, zoomedHandleSize ) )
			linesToBeDrawn.setLineWidth_( handleStroke )
			linesToBeDrawn.stroke()
			circlesToBeDrawn.setLineWidth_( handleStroke )
			circlesToBeDrawn.stroke()

			smooths = NSBezierPath.alloc().init()
			smoothToBeFilled = nodesLists[1]
			for thisPoint in smoothToBeFilled:
				smooths.appendBezierPath_( self.roundDotForPoint( thisPoint, zoomedHandleSize ) )
			colorData = Glyphs.defaults["GSColorNodeSmooth"]
			color = NSUnarchiver.unarchiveObjectWithData_(colorData)
			color.set()
			smooths.fill()

			sharps = NSBezierPath.alloc().init()
			sharpToBeFilled = nodesLists[2]
			for thisPoint in sharpToBeFilled:
				sharps.appendBezierPath_( self.squareDotForPoint( thisPoint, zoomedHandleSize ) )
			colorData = Glyphs.defaults["GSColorNodeCorner"]
			color = NSUnarchiver.unarchiveObjectWithData_(colorData)
			color.set()
			sharps.fill()

			offCurves = NSBezierPath.alloc().init()
			sharpToBeFilled = nodesLists[3]
			for thisPoint in sharpToBeFilled:
				offCurves.appendBezierPath_( self.roundDotForPoint( thisPoint, zoomedHandleSize ) )
			NSColor.grayColor().set()
			offCurves.fill()
		except Exception, e:
			Glyphs.showMacroWindow()
			print "Show Black Fill error (foreground): %s" % e
