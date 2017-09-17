#!/usr/bin/env python3
# coding=utf-8

from xml.dom.minidom import parse, parseString

from geninterface import *
from xmlnamedef import *
from xmlparse import *


class CppGen(ClassFileInterface):
    def __init__(self, xmlnode, classdir):
        ClassFileInterface.__init__(self, xmlnode, classdir)

    def GetFileExtName(self):
        return ".h"

    def GetClassDir(self):
        return self.classdir

    def GenFileHead(self):
        self.str += "#ifndef " + self.GenFileDefined() + enter
        self.str += "#define " + self.GenFileDefined() + enter + enter


    def GenFileEnd(self):
        self.str += enter
        self.str += "#endif//" + self.GenFileDefined() + enter
        return self.str

    def GenImports(self):
        for ip in self.GetImports():
            self.str += ip.getAttribute(name) + enter
        self.str += enter

        for val in self.xmlnode.getElementsByTagName(declareclass):
            cls = val.getAttribute(name) 
            if cls and val.getAttribute(outsideclass):
                self.str += "class " + cls + ";" + enter 
        return self.str

    def GenNameSpaceHead(self):
        if self.xmlnode.getAttribute(namespace):
            ns = self.xmlnode.getAttribute(namespace)
            self.str += "namespace " + ns + enter +  "{" + enter
        return self.str

    def GenNameSpaceEnd(self):
        if self.xmlnode.getAttribute(namespace):
            self.str += enter
            ns = self.xmlnode.getAttribute(namespace)
            self.str += "} // namespace " + ns + enter
        return self.str

    def GenClassHead(self):
        self.str += enter

        for val in self.xmlnode.getElementsByTagName(declareclass):
            cls = val.getAttribute(name) 
            if cls and val.getAttribute(outsideclass):
                continue
            self.str += "class " + cls + ";" + enter 

        self.GenClassAnnotation()
        self.GenTemplate()
        self.str += "class " + self.xmlnode.getAttribute(name) + self.GenClassInheritance() + enter
        self.str += "{" + enter
        return self.str

    def GenClassInheritance(self):
        str = ""
        ih = self.xmlnode.getAttribute(inheritance)
        if ih:
            str += " : public " + self.xmlnode.getAttribute(inheritance)
        return str

    def GenTemplate(self):
        tmpl = self.xmlnode.getAttribute(template)
        if tmpl:
            self.str += "template" + tmpl + enter

    def GenClassEnd(self):
        self.str += "}; // class " + self.classname  + enter
        return self.str

    def GenFileDefined(self):
        return   self.classname.upper() + "_H" 

    def GenTypeDef(self):
        if self.xmlnode.getElementsByTagName(typedef):
            self.str += "public:" + enter
        for td in self.xmlnode.getElementsByTagName(typedef):
            self.str += GetTab(1) + td.getAttribute(name) + enter
        return self.str

    def GenDefConstor(self):
        if self.xmlnode.getAttribute(default) != "true":
            return ""
        self.str += "public:" + enter
        ClassFileInterface.GenDefConstor(self)
        self.str += GetTab(1) + ":" + enter  
        for val in self.GetValuesNodeList():
            if val.getAttribute(capacity):
                continue
            str = val.getAttribute(name) + "(" + val.getAttribute(default) + ")," + enter
            self.str += GetTab(1) + " " + str 
        self.str = self.str[:-2] + enter
        self.str += GetTab(1) + "{" + enter
        for val in self.GetValuesNodeList():
            vn = CppClassValueNode(val)
            if val.getAttribute(capacity):
                self.str += vn.GenClearCollection(vn.GetName())
        self.str += GetTab(1) + "}" + enter
        return self.str

    def GenArgConstor(self):
        if self.xmlnode.getAttribute(argconstor) != "true":
            return ""
        self.str += "public:" + enter
        ClassFileInterface.GenArgConstor(self)
        for val in self.GetValuesNodeList():
            if val.getAttribute(capacity):
                continue
            vn = CppClassValueNode(val)
            str = val.getAttribute(name) + "(" + vn.GetTmpName() + ")," + enter
            self.str += GetTab(1) + " " + str 
        self.str = self.str[:-2]  + enter 
        self.str += GetTab(1) + "{" + enter
        for val in self.GetValuesNodeList():
            vn = CppClassValueNode(val)
            if val.getAttribute(capacity):
                self.str += vn.GenMemcpy( "rfh." + vn.GetName())
        self.str += GetTab(1) + "}" + enter
        return self.str

    def GenCopyConstor(self):
        if self.xmlnode.getAttribute(copy) == "delete":
            self.str += GetTab(1) + self.classname + "(const " + self.classname + "&) = delete;" + enter
            return self.str
        if self.xmlnode.getAttribute(copy) == "default":
            return ""
        self.str += "public:" + enter
        self.str += GetTab(1) + self.classname + "(const " + self.classname + " & rhf)" + enter
        self.str += GetTab(1) + ":" + enter  
        for val in self.GetValuesNodeList():
            if val.getAttribute(capacity):
                continue
            vn = CppClassValueNode(val)
            self.str += GetTab(1) + " " + vn.GetName() + "(rhf." + vn.GetName() + ")," + enter
        self.str = self.str[:-2]  + enter 
        self.str += GetTab(1) + "{" + enter
        for val in self.GetValuesNodeList():
            vn = CppClassValueNode(val)
            if val.getAttribute(capacity):
                self.str += vn.GenMemcpy(vn.GetName())
        self.str += GetTab(1) + "}" + enter
        return self.str
    
    def GenAssignOp(self):
        if self.xmlnode.getAttribute(assign) == "delete":
            self.str += GetTab(1) + self.classname + "& operator=(const " + self.classname + "&) = delete;" + enter
            return self.str
        if self.xmlnode.getAttribute(copy) == "default":
            return ""
        self.str += "public:" + enter
        self.str += GetTab(1) + self.classname + " & operator=(const " + self.classname + " & rhf)" + enter
        self.str += GetTab(1) + "{" + enter
        self.str += GetTab(2) + "if (this == &rhf){return *this;}" + enter
        for val in self.GetValuesNodeList():
            vn = CppClassValueNode(val)
            if val.getAttribute(capacity):
                self.str += vn.GenClearCollection(vn.GetName())
                self.str += GetTab(2) + "memcpy(this->" + vn.GetName() + ", rhf." + vn.GetName() + ", sizeof(" + vn.GetName() + "));" + enter
                continue
            self.str += GetTab(2) + "this->" + vn.GetName() + " = rhf." + vn.GetName() + ";" + enter
        self.str += GetTab(2) + "return *this;" + enter
        self.str += GetTab(1) + "}" + enter
        return self.str

    def GenDestructor(self):
        if self.xmlnode.getAttribute(customdes):
            return self.str
        self.str += "public:" + enter
        if self.xmlnode.getAttribute(polymorphic) != "true":
            self.str += GetTab(1) + "~" + self.classname + "(){}" + enter
            return ""
        self.str += GetTab(1) + "virtual ~" + self.classname + "(){}" + enter
        return self.str

    def GenClone(self):
        return self.str

    def GenClassInnerDef(self):
        return self.str

    def GenMyFun(self):
        self.GenMemberFun(pubfun)
        for val in self.GetValuesNodeList():
            vn = CppClassValueNode(val)
            self.str += vn.GenAddCollection()
            self.str += vn.GenGetCollection()
            self.str += vn.GenGetCollectionCapacity()
        self.GenMemberFun(prvfun)
        return self.str

    def GenMemberFun(self, authority):
        self.GenAuthorityFlag(authority)
        for pf in self.xmlnode.getElementsByTagName(authority):
            if pf.getAttribute(annotation):
                self.str += GetTab(1) + "//" + pf.getAttribute(annotation) + enter
            self.str += GetTab(1) + pf.getAttribute(name) + enter
            if pf.getAttribute(group) == begin:
                pass
            elif pf.getAttribute(group) == body:
                pass
            elif pf.getAttribute(group) == end:
                self.str += enter
            else:
                self.str += enter
        return self.str

    def GenAuthorityFlag(self, authority):
        if authority == "pubfun":
            self.str += "public:" + enter
        if authority == "prvfun":
            self.str += "private:" + enter
        return self.str

    def GenClassValues(self):
        self.str += enter + "////////////////GetSetFun" + enter
        self.str += "public:" + enter
        #GetSet
        for val in self.GetValuesNodeList():
            vn = CppClassValueNode(val)
            self.str += vn.GenSetFun()
            self.str += vn.GenGetFun()

        self.str += "private:" + enter
        for val in self.GetValuesNodeList():
            vn = CppClassValueNode(val)
            self.str += vn.GenValueDef()

        return self.str

    def GenClearFun(self):
        self.str += "public:" + enter
        self.str += GetTab(1) + "void Clear(void)" + enter  
        self.str += GetTab(1) + "{" + enter
        for val in self.GetValuesNodeList():
            vn = CppClassValueNode(val)
            self.str += vn.GenClearFun()
        self.str +=  GetTab(1) +  "}" + enter + enter
        return self.str


class CppClassValueNode(ClassValueNode):
    def __init__(self, valuenode):
        ClassValueNode.__init__(self, valuenode)
        index = self.type.find("[")
        if index != -1:
            self.deftype = self.type[:index] + " " + self.name + self.type[index:]
        else:
            self.deftype = self.type + " " + self.name

        if self.rettype:
            str = ""
        else:
            self.rettype = self.type

        classnamelist = ClassNameList()
        if self.handletype in classnamelist.GetClassNameList():
            self.argref += "& "

        setfunref = ""
        if self.capacity:
            setfunref = ""
        else:
            setfunref = self.argref

        if self.std:
            setfunref = "& "

        if index != -1:
            self.argtypedef = self.type[:index] + " " + setfunref + self.GetTmpName() + self.type[index:]
        else:
            self.argtypedef = self.type + " " + setfunref + self.GetTmpName()



def cppmain():
    xml = XmlParse("example.xml")
    xml.Parse()
    defaultdir = "genfile/"
    classnamelist = ClassNameList()
    classnamelist.SetClassNameList(xml.GetClassNameList())
    for xmlnode in xml.GetClassNodeList():
        cfi = CppGen(xmlnode, defaultdir)
        file = FileWrite()
        file.Write(cfi)

#cppmain()
