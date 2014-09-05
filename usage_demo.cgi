#!/usr/bin/env python

print "Content-Type: text/html"
print

import cgitb
cgitb.enable()

import pyWaferMapSVG as svg
map = svg.pyWaferMapSVG(450, "down")
map.setDieMaps(10,20,[(200,150,'green'),(100,60),(170,200,'red','bad die')])
result = map.makeSVG()

print """<!DOCTYPE html>
			<html>
				<head>
					<meta http-equiv="X-UA-Compatible" content="IE=edge" />
					<title>Wafer Map Demo</title>
				</head>
			<body>"""

print result

print """</body></html>"""