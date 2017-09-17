#!/usr/bin/env python3
# coding=utf-8

from xml.dom.minidom import parse, parseString

from geninterface import *
from xmlnamedef import *

class XmlParse:
    def __init__(self, xmlfile):
        self.xmlfile = xmlfile
        self.classnamelist = []
        self.classnodelist = []
        self.doc = ""

    def GetClassNodeList(self):
        return self.classnodelist

    def GetClassNameList(self):
        return self.classnamelist;

    def Parse(self):
        self.doc = parse(self.xmlfile)
        self.classnodelist = self.doc.getElementsByTagName("class")
        for classname in self.classnodelist:
            self.classnamelist.append(classname.getAttribute(name))
        
