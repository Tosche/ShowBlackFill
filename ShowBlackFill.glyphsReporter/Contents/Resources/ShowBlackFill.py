#!/usr/bin/env python
# encoding: utf-8

import objc
from Foundation import *
from AppKit import *
import sys, os, re

MainBundle = NSBundle.mainBundle()
path = MainBundle.bundlePath() + "/Contents/Scripts"
if not path in sys.path:
	sys.path.append( path )

import GlyphsApp

GlyphsReporterProtocol = objc.protocolNamed( "GlyphsReporter" )

class ShowBlackFill ( NSObject, GlyphsReporterProtocol ):
	
	def init( self ):
		try:
			#Bundle = NSBundle.bundleForClass_( NSClassFromString( self.className() ));
			return self
		except Exception as e:
			self.logToConsole( "init: %s" % str(e) )
	
	def interfaceVersion( self ):
		try:
			return 1
		except Exception as e:
			self.logToConsole( "interfaceVersion: %s" % str(e) )
	
	def title( self ):
		try:
			return "Black Fill"
		except Exception as e:
			self.logToConsole( "title: %s" % str(e) )
	
	def keyEquivalent( self ):
		try:
			return None
		except Exception as e:
			self.logToConsole( "keyEquivalent: %s" % str(e) )
	
	def modifierMask( self ):
		try:
			return 0
		except Exception as e:
			self.logToConsole( "modifierMask: %s" % str(e) )
	
	def setController_( self, Controller ):
		self.controller = Controller
	
	def getScale( self ):
		"""
		Returns the current scale factor of the Edit View UI.
		Divide any scalable size by this value in order to keep the same pixel size.
		"""
		try:
			return self.controller.graphicView().scale()
		except:
			self.logToConsole( "Scale defaulting to 1.0" )
			return 1.0
	
	def getNodeSize( self ):
		"""
		Returns the current handle size as set in user preferences.
		"""
		try:
			Selected = NSUserDefaults.standardUserDefaults().integerForKey_( "GSHandleSize" )
			if Selected == 0:
				return 5.0
			elif Selected == 2:
				return 10.0
			else:
				return 7.0
		except:
			self.logToConsole( "HandleSize defaulting to 7.0" )
			return 7.0
	
	def getListOfNodesToBeMarked( self, thisLayer ):
		"""
		Returns a list of all On-curve nodes.
		"""
		try:
			returnList = []
		
			for thisPath in thisLayer.paths:
				for i in range( len( thisPath.nodes )):
					thisNode = thisPath.nodes[ i ]
					returnList.append( thisNode )
							
			return returnList
		except Exception as e:
			self.logToConsole( "getListOfNodesToBeMarked: " + str(e) )

	def getListOfSelectedSmooth( self, thisLayer ):
		"""
		Returns a list of all selected smooth On-curve nodes.
		"""
		try:
			returnList = []
			currentSelection = thisLayer.selection()
		
			for thisObject in currentSelection:
				if type( thisObject ) == GSNode:
					if thisObject.connection == 4096:
						returnList.append( thisObject )
			# It doesn't work. Disables all nodes when connected.
			#if not currentSelection.closed:
			#	del returnList[0, -1]
			return returnList
		except Exception as e:
			self.logToConsole( "getListOfSelectedNodes_ " + str(e) )

	def getListOfSelectedSharp( self, thisLayer ):
		"""
		Returns a list of all selected sharp On-curve nodes.
		"""
		try:
			returnList = []
			currentSelection = thisLayer.selection()
		
			for thisObject in currentSelection:
				if type( thisObject ) == GSNode:
					if thisObject.type != 65 and thisObject.connection !=4096:
							returnList.append( thisObject )
			# It doesn't work. Disables all nodes when connected.
			#if not currentSelection.closed:
			#	del returnList[0, -1]
			return returnList
		except Exception as e:
			self.logToConsole( "getListOfSelectedNodes_ " + str(e) )

	def getListOfSelectedOffCurve( self, thisLayer ):
		"""
		Returns a list of all selected Off-curve nodes.
		"""
		try:
			returnList = []
			currentSelection = thisLayer.selection()
		
			for thisObject in currentSelection:
				if type( thisObject ) == GSNode:
					if thisObject.type == 65:
						returnList.append( thisObject )
			return returnList
		except Exception as e:
			self.logToConsole( "getListOfSelectedNodes_ " + str(e) )
	
	def getListOfHandlesToBeMarked( self, thisLayer ):
		"""
		Returns a list of Handles that need to be outlined.
		"""
		try:
			returnList = []
			currentSelection = thisLayer.selection()
		
			for thisPath in thisLayer.paths:
				thisPathLength = len( thisPath.nodes )

				for i in range( len( thisPath.nodes )):
					thisNode = thisPath.nodes[ i ]
					if thisNode in currentSelection:
						prevNode = thisPath.nodes[ (i-1) % thisPathLength]
						nextNode = thisPath.nodes[ (i+1) % thisPathLength]
					
						if thisNode.type == 65:
							# a selected off-curve
							if prevNode.type != 65:
								returnList.append( (prevNode, thisNode) )
								if not nextNode in currentSelection:
									returnList.append( ( thisPath.nodes[ (i+2) % thisPathLength], nextNode ) )
							elif nextNode.type != 65:
								returnList.append( (nextNode, thisNode) )
								if not prevNode in currentSelection:
									returnList.append( ( thisPath.nodes[ (i-2) % thisPathLength], prevNode ) )
						else:
							# a selected on-curve
							if prevNode.type == 65 and not prevNode in currentSelection:
								returnList.append( (thisNode, prevNode) )
								prevPrevNode = thisPath.nodes[ (i-2) ]
								prevPrevPrevNode = thisPath.nodes[ (i-3) ]
								if prevPrevNode not in currentSelection and prevPrevPrevNode not in currentSelection:
									returnList.append( (prevPrevPrevNode, prevPrevNode) )
							if nextNode.type == 65 and not nextNode in currentSelection:
								returnList.append( (thisNode, nextNode) )
								nextNextNode = thisPath.nodes[ (i+2) % thisPathLength ]
								nextNextNextNode = thisPath.nodes[ (i+3) % thisPathLength ]
								if nextNextNode not in currentSelection and nextNextNextNode not in currentSelection:
									returnList.append( (nextNextNextNode, nextNextNode) )
		
			return list(set(returnList))
		except Exception as e:
			self.logToConsole( "getListOfHandlesToBeMarked_ " + str(e) )
			
		
	
	def markerForPoint( self, thisPoint, markerWidth ):
		"""
		Returns a circle with thisRadius around thisPoint.
		"""
		try:
			myRect = NSRect( ( thisPoint.x - markerWidth * 0.5, thisPoint.y - markerWidth * 0.5 ), ( markerWidth, markerWidth ) )
			return NSBezierPath.bezierPathWithOvalInRect_( myRect )
		except Exception as e:
			self.logToConsole( "markerForPoint_ " + str(e) )
			
	
	def drawForegroundForLayer_( self, Layer ):
		"""
		Fills closed outline, outlines handles, and paints nodes.
		"""
		#Black fill
		try:
						NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.0, 0.0, 0.0, 0.85 ).set() # sets RGBA values between 0.0 and 1.0
						Layer.bezierPath().fill()
		except Exception as e:
			self.logToConsole( "drawForegroundForLayer_: %s" % str(e) )

		try:
			NodeSize = self.getNodeSize()
			Scale = self.getScale()
			circleRadius = NodeSize / Scale
			handleStroke = 1.0 / Scale
			
			# Selected handles
			NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.5, 0.5, 0.5, 0.5).set()
			circlesToBeDrawn = NSBezierPath.alloc().init()
			linesToBeDrawn   = NSBezierPath.alloc().init()
			for thisPointPair in self.getListOfHandlesToBeMarked( Layer ):
				fromPoint = thisPointPair[0]
				toPoint   = thisPointPair[1]
				linesToBeDrawn.moveToPoint_( NSPoint(fromPoint.x, fromPoint.y) )
				linesToBeDrawn.lineToPoint_( NSPoint(toPoint.x, toPoint.y) )
				circlesToBeDrawn.appendBezierPath_( self.markerForPoint( toPoint, circleRadius ) )
			linesToBeDrawn.setLineWidth_( handleStroke )
			linesToBeDrawn.stroke()
			circlesToBeDrawn.setLineWidth_( handleStroke )
			circlesToBeDrawn.stroke()

			# Unselected nodes
			NSColor.colorWithCalibratedRed_green_blue_alpha_( 1.0, 1.0, 1.0, 0.15 ).set()
			circlesToBeDrawn = NSBezierPath.alloc().init()
			for thisPoint in self.getListOfNodesToBeMarked( Layer ):
				circlesToBeDrawn.appendBezierPath_( self.markerForPoint( thisPoint, circleRadius ) )
			circlesToBeDrawn.fill()
			
			# Selected Smooth On-curve
			NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.0, 0.7, 0.4, 0.3 ).set()
			circlesToBeDrawn = NSBezierPath.alloc().init()
			for thisPoint in self.getListOfSelectedSmooth( Layer ):
				circlesToBeDrawn.appendBezierPath_( self.markerForPoint( thisPoint, circleRadius ) )
			circlesToBeDrawn.fill()

			# Selected Sharp On-Curve
			NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.2, 0.4, 0.8, 0.3 ).set()
			circlesToBeDrawn = NSBezierPath.alloc().init()
			for thisPoint in self.getListOfSelectedSharp( Layer ):
				circlesToBeDrawn.appendBezierPath_( self.markerForPoint( thisPoint, circleRadius ) )
			circlesToBeDrawn.fill()

			# Selected Off-curve
			NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.5, 0.5, 0.5, 0.2 ).set()
			circlesToBeDrawn = NSBezierPath.alloc().init()
			for thisPoint in self.getListOfSelectedOffCurve( Layer ):
				circlesToBeDrawn.appendBezierPath_( self.markerForPoint( thisPoint, circleRadius ) )
			circlesToBeDrawn.fill()

		except Exception as e:
			self.logToConsole( "drawForegroundForLayer_ " + str(e) )
	
	def drawBackgroundForLayer_( self, Layer ):
		"""
		Whatever you draw here will be displayed BEHIND the paths.
		"""
		try:
			pass
		except Exception as e:
			self.logToConsole( "drawBackgroundForLayer_: %s" % str(e) )
	
	def drawBackgroundForInactiveLayer_( self, Layer ):
		"""
		Whatever you draw here will be displayed behind the paths, but for inactive masters.
		"""
		try:
			pass
		except Exception as e:
			self.logToConsole( "drawBackgroundForInactiveLayer_: %s" % str(e) )
	
	def needsExtraMainOutlineDrawingForInactiveLayer_( self, Layer ):
		"""
		Return False to disable the black outline. Otherwise remove the method.
		"""
		return False
	
	def getScale( self ):
		"""
		self.getScale() returns the current scale factor of the Edit View UI.
		Divide any scalable size by this value in order to keep the same apparent pixel size.
		"""
		try:
			return self.controller.graphicView().scale()
		except:
			self.logToConsole( "Scale defaulting to 1.0" )
			return 1.0
	
	def setController_( self, Controller ):
		"""
		Use self.controller as object for the current view controller.
		"""
		try:
			self.controller = Controller
		except Exception as e:
			self.logToConsole( "Could not set controller" )
	
	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "Show %s plugin:\n%s" % ( self.title(), message )
		NSLog( myLog )
