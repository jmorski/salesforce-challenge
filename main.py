#author : Jeff Morski

import sys
filename = "proga.dat"
packageList = []

class package:
    def __init__(self,name):
        self.name = name
        self.dependents = []
        self.isInstalled = False
        #requested by the user
        self.explicitlyInstalled = False
        #needed by another package
        self.implicitlyInstalled = False

    def getName(self):
        return self.name

    def setName(self,name):
        self.name = name

    def addDependents(self,pkg):
        self.dependents.append(pkg)

    def getDependents(self):
        return self.dependents

    def isInstalled(self):
        return self.isInstalled

    def setInstalled(self,explicit,implicit):
        if self.isInstalled:
            return self.isInstalled
        for x in self.getDependents():
            x.setInstalled(False,True)
        print "\t Installing %s" % self.getName()
        self.isInstalled = True
        self.explicitlyInstalled = explicit
        self.implicitlyInstalled = implicit

    def dependsOn(self,deppkg):
        for pkg in self.getDependents():
            if pkg.getName() == deppkg.getName():
                return True
            else:
                return False

    def canBeUninstalled(self , explicitRemoval):
        if not explicitRemoval and self.explicitlyInstalled:
            return False
        for pkg in packageList:
            if pkg.isInstalled and pkg.dependsOn(self):
                return False
        else:
            return True

    def uninstall(self):
            print "\t Removing %s" % self.getName()
            self.isInstalled = False
            self.implicitlyInstalled = False
            self.explicitlyInstalled = False

            for pkg in self.getDependents():
                if pkg.canBeUninstalled(False):
                    pkg.uninstall()

def getCreatePackage(name):
    curpack = None
    for pkg in packageList:
        if pkg.getName() == name:
            curpack = pkg
    if curpack is None:
        curpack = package(name)
        packageList.append(curpack)
    return curpack

def stripBlanksFromList(list):
    list = [x for x in list if x != ""]
    return list

def processLine(line):
    commandparts = line.split(" ")
    if commandparts[0] == "DEPEND":
        commandparts = stripBlanksFromList(commandparts)
        for part in commandparts:
            if part != "DEPEND":
                getCreatePackage(part)
            currentpackage = getCreatePackage(commandparts[1])
        for x in range(2,len(commandparts)):
            currentpackage.addDependents(getCreatePackage(commandparts[x]))
    elif commandparts[0] == "INSTALL":
        commandparts = stripBlanksFromList(commandparts)
        for part in commandparts:
            if part != "INSTALL":
                pkg = getCreatePackage(part)
                if pkg.isInstalled:
                    print "\t %s is already installed" % pkg.getName()
                pkg.setInstalled(True,False)
    elif commandparts[0] == "REMOVE":
        commandparts = stripBlanksFromList(commandparts)
        for part in commandparts:
            if part != "REMOVE":
                pkg = getCreatePackage(part)
                if not pkg.isInstalled:
                    print "\t %s is not installed" % pkg.name
                    return
                else:
                    if pkg.canBeUninstalled(True):
                        pkg.uninstall()
                    else:
                        print "\t %s is still needed" % pkg.name
    elif commandparts[0] == "LIST":
        for pkg in packageList:
            if pkg.isInstalled:
                print "\t %s" %pkg.getName()
    else:
        print "Invalid Command"
        sys.exit()

def main():
    try:
        lines = tuple(open(filename,'r'))
    except IOError:
        print "Could not not open file %s ",filename
    for line in lines:
        line = line.rstrip()
        if line == "END":
            sys.exit(0)
        print '%s' % line
        processLine(line)

if __name__ == "__main__":
    main()
