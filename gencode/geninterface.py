#!/usr/bin/env python3
# coding=utf-8

import copy

from xmlnamedef import *


tab = "\t"
enter = "\n"


class Singleton(object):
    def __new__(cls, *args, **argc):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **argc)
        return cls._instance

class ClassNameList(Singleton):
    classnamelist = []

    def SetClassNameList(self, classnamelist):
        for classname in classnamelist:
            self.classnamelist.append(classname)

    def GetClassNameList(self):
        return self.classnamelist

def GetTab(count):
    strret = ""
    for i in range(count):
        strret += tab
    return strret




class ClassFileInterface:
    def __init__(self, xmlnode, classdir):
        self.str = ""
        self.xmlnode = xmlnode
        self.classname = xmlnode.getAttribute(name)
        tmpdir = self.xmlnode.getAttribute(gendir)
        if tmpdir:
            self.classdir = tmpdir
        else:
            self.classdir = classdir
        self.valuenodelist = self.xmlnode.getElementsByTagName(value)
        self.imports = self.xmlnode.getElementsByTagName(include)
        self.filename = xmlnode.getAttribute(filename)

    def GetFileContext(self):
        return self.str;

    def GetClassName(self):
        return self.classname

    def GetFileExtName(self):
        return ""

    def GetFileName(self):
        if self.filename:
            return self.filename + self.GetFileExtName();
        return self.GetClassName() + self.GetFileExtName();
    
    def Process(self):
        self.GenFileHead()
        self.GenImports()
        self.GenNameSpaceHead()
        self.GenClassHead()
        self.GenClassBody()
        self.GenClassEnd()
        self.GenNameSpaceEnd()
        self.GenFileEnd()
        return self.str;

    def GetClassDir(self):
        return self.classdir

    def GenFileHead(self):
        return self.str

    def GenFileEnd(self):
        return self.str

    def GenImports(self):
        return self.str

    def GenNameSpaceHead(self):
        return self.str

    def GenNameSpaceEnd(self):
        return self.str

    def GenClassHead(self):
        return self.str

    def GenClassBody(self):
        self.GenTypeDef()
        self.GenDefConstor()
        self.GenArgConstor()
        self.GenCopyConstor()
        self.GenAssignOp()
        self.GenDestructor()
        self.GenClearFun()
        self.GenClone()
        self.GenMyFun()
        self.GenClassValues()
        return self.str

    def GenClassEnd(self):
        return self.str

    def GenTypeDef(self):
        return self.str

    def GenClassAnnotation(self):
        if self.xmlnode.getAttribute(annotation):
            self.str += "//" + self.xmlnode.getAttribute(annotation) + enter
        return self.str

    def GenDefConstor(self):
        self.str += GetTab(1) + self.classname + "()" + enter
        return self.str

    def GenArgConstor(self):
        self.str += GetTab(1) + self.classname + "( "
        for val in self.GetValuesNodeList():
            vn = ClassValueNode(val)
            self.str += vn.GetType() + " " + vn.GetTmpName() + ", "
        self.str = self.str[:-2] 
        self.str += GetTab(1) +  ")" + enter
        self.str += GetTab(1) + ":" + enter  
        return self.str

    def GenCopyConstor(self):
        return self.str
    
    def GenAssignOp(self):
        return self.str

    def GenDestructor(self):
        return self.str

    def GenClone(self):
        return self.str

    def GenClassInnerDef(self):
        return self.str

    def GenMyFun(self):
        return self.str

    def GenClassValues(self):
        return self.str

    def GenAfterIcldBeforeClass(self):
        return self.str

    def GetValuesNodeList(self):
        return self.valuenodelist

    def GetImports(self):
        return self.imports

    def GenClearFun(self):
        return self.str


####################

class ClassValueNode:
    def __init__(self, valuenode):
        self.valuenode = valuenode
        self.name = valuenode.getAttribute(name)
        self.type = valuenode.getAttribute(type)
        self.annotation = valuenode.getAttribute(annotation)
        self.retref = valuenode.getAttribute(retref)
        self.collectionsize = valuenode.getAttribute(collectionsize)
        self.capacity = valuenode.getAttribute(capacity)
        self.rettype = valuenode.getAttribute(rettype)
        self.default = valuenode.getAttribute(default)
        self.deftype = ""
        self.argtypedef = ""
        self.argref = ""
        self.handletype = self.type
        self.std = valuenode.getAttribute(std) 

        hi = valuenode.getAttribute(type).find("[")
        if hi != -1:
            self.handletype = self.type[:hi]

    def GenSetFun(self):
        if self.valuenode.getAttribute(nosetfun):
            return "";
        str = GetTab(1)
        str += "void Set" + self.GetAfterHandleName(self.name) + "(" +  self.GetArgType() + ")" + enter
        str += GetTab(1) + "{" + enter
        if self.collectionsize:
            str += self.GenMemcpy(self.GetTmpName())
        else:
            str += GetTab(2)
            str += "this->" + self.name + " = " + self.GetTmpName() + ";" + enter

        str += GetTab(1) + "}" + enter
        return str 

    def GenGetFun(self):
        if self.valuenode.getAttribute(nogetfun):
            return "";
        str = ""
        str += GetTab(1) + "const " + self.GetRetType() + " "
        if self.retref:
            str += "& "
        str += "Get" + self.GetAfterHandleName(self.name) + "() const" + enter
        str += GetTab(1) + "{" + enter
        str += GetTab(2)
        str += "return " + self.GenGetRetValue() + ";" + enter

        str += GetTab(1) + "}" + enter
        return str 

    def GenGetRetValue(self):
        str = ""
        if self.rettype.lower().find("char*") != -1:
            str += "static_cast<const char*>(this->" + self.name + ")"
        else:
            str = "this->" + self.name
        return str

    def GetAfterHandleName(self, valname):
        valname = valname[3:]
        return valname


    def GenValueDef(self):
        str = ""
        str += GetTab(1) + self.GetValueDef() + ";"
        if self.annotation:
            str += GetTab(2) + "//" + self.annotation
        str += enter
        return str

    def GetCapacity(self, valuenode):
        return self.capacity

    def GetTmpName(self):
        return "t" + self.name.lstrip("m_")

    def GetArgRef(self, valuenode):
        return ""

    def GenCopyCollectionValue(self):
        return ""

    def GetType(self):
        return self.type

    def GetRetType(self):
        return self.rettype

    def GetArgType(self):
        return self.argtypedef

    def GetValueDef(self):
        return self.deftype

    def GetHandleType(self):
        return self.deftype

    def GetName(self):
        return self.name

    def GenMemcpy(self, src):
        str = ""
        if self.capacity:
            str += self.GenClearCollection(src)
            str += GetTab(2)
            str += "memcpy(this->" + self.name + ", " + src + ", sizeof(" + self.name + "));" + enter
        return str
    
    def GenClearCollection(self, src):
        str = ""

        classnamelist = ClassNameList()
        if self.rettype and self.rettype.lower().find("char") != -1:
            str += GetTab(2)
            str += "memset(this->" + self.name + ", 0, " + "sizeof(" + self.name + "));" + enter
        elif self.rettype and self.handletype in classnamelist.GetClassNameList():
            str += GetTab(2)
            str += "for ( int i = 0; i < " + self.capacity + "; ++i)" + enter
            str += GetTab(2)
            str += "{" + enter
            str += GetTab(3) + self.name + "[i].Clear();" + enter
            str += GetTab(2)
            str += "}" + enter
        return str

    def GenClearFun(self):
        str = ""
        if self.std:
            str += GetTab(2)
            str += self.name + ".clear();" + enter
            return str
        if self.capacity:
            str += self.GenClearCollection(self.name)
        else:
            classnamelist = ClassNameList()
            if self.type in classnamelist.GetClassNameList():
                str += GetTab(2) +  self.name + ".Clear();" + enter
            else:
                str += GetTab(2) +  self.name + " = " + self.default + ";" + enter
        return str

    def GenAddCollection(self):
        str = ""
        classnamelist = ClassNameList()
        if self.capacity and self.handletype in classnamelist.GetClassNameList():
            str += GetTab(1)
            str += "void Add" + self.GetAfterHandleName(self.name) + "( const  " +  self.handletype + " " +  self.argref + " " + self.GetTmpName() + ")" + enter
            str += GetTab(1) 
            str += "{" + enter
            str += GetTab(2) 
            str += "if ( !(0 <= " + self.collectionsize + " && " + self.collectionsize + " < " + self.capacity + ") )" + enter
            str += GetTab(2) + "{" + enter
            str += GetTab(3) + " return;" + enter
            str += GetTab(2) + "}" + enter

            str += GetTab(2) + self.name + "[" + self.collectionsize + "++] = " + self.GetTmpName() + ";" +  enter
            str += GetTab(1) 
            str += "}" + enter
        return str

    def GenGetCollection(self):
        str = ""
        classnamelist = ClassNameList()
        if self.capacity and self.handletype in classnamelist.GetClassNameList():
            str += GetTab(1)
            str += self.handletype + " & Get" + self.GetAfterHandleName(self.name) + "(int tnIndex)" + enter
            str += GetTab(1) 
            str += "{" + enter
            str += GetTab(2) 
            str += "if ( !(0 <= tnIndex  && tnIndex < " + self.capacity + ") )" + enter
            str += GetTab(2) + "{" + enter
            str += GetTab(3) + " static " + self.handletype + " " + self.GetTmpName() + ";" + enter
            str += GetTab(3) + " return " + self.GetTmpName() + ";" + enter
            str += GetTab(2) + "}" + enter

            str += GetTab(2) + "return " + self.name + "[tnIndex]"  + ";" +  enter
            str += GetTab(1) 
            str += "}" + enter
        return str

    def GenGetCollectionCapacity(self):
        str = ""
        classnamelist = ClassNameList()
        if self.capacity and self.handletype in classnamelist.GetClassNameList():
            str += GetTab(1) + "int Get" + self.GetAfterHandleName(self.name) + "Capacity(){ return " + self.capacity + "; }" + enter
        return str
        

class FileWrite:
    def __init__(self):
        self.dir = "";

    def Write(self, cfi):
        cfi.Process()
        f = open(cfi.GetClassDir() + cfi.GetFileName(), 'w')
        f.write(cfi.GetFileContext())
        f.close();




