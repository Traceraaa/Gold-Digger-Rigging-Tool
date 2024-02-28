import maya.cmds as cmds
import math

global selectedOBJ
global updateCopyNum
global tread_curve
global change_tread
global oldobj
global defobj
global tread_num
global proxy_created

oldobj=None
selectedOBJ=None
updateCopyNum=25
change_tread=False
tread_num = 1
proxy_created = False

#2this is window function but not running first
def makewindow():
    winName="TreadBuilder"
    if cmds.window(winName,q=True,ex=True):
        cmds.deleteUI(winName)
    #now if all good we make the window
    cmds.window(winName,w=300, h=350, s=False)
    mainCL = cmds.columnLayout()

    UI_WARNING_BGC = [1, 1, 0]
    #Initialize
    makewindow.uiInitFrame = cmds.frameLayout(l="Initialize", w=500, cll=True)
    makewindow.uiInitCL = cmds.columnLayout()

    cmds.text(l="Creating two locators in the scene. Front and Back")
    makewindow.initButton=cmds.button(l="Initialize",c="initFunc()")
    cmds.setParent(mainCL)
    cmds.separator(w=500)

    #Make Curve
    makewindow.uiCurveFrame = cmds.frameLayout(l="Create Curve", w=500, cll=True, en=False)
    makewindow.uiCurveCL = cmds.columnLayout()
    
    cmds.text(l="Requirement!", fn="boldLabelFont", bgc=UI_WARNING_BGC)
    cmds.text(l="Position the two locators at the front and back end of your curve. And then hit the button")
    makewindow.MakeCurveBTN=cmds.button(l="Make Tread Curve",c="MakeCurve()",en=False)
    cmds.setParent(mainCL)
    cmds.separator(w=500)
    
    #Create Tread
    makewindow.uiCreateFrame = cmds.frameLayout(l="Create Tread", w=500, cll=True, en=False)
    makewindow.uiCreateCL = cmds.columnLayout()

    cmds.text(l="Requirement!", fn="boldLabelFont", bgc=UI_WARNING_BGC)
    cmds.text(l="Select default or pick your own tread peice. Hit the Update button to observe the change")
    makewindow.peicesel = cmds.radioButtonGrp( label='Pick Tread Peice ', labelArray2=['Default', 'Pick your own peice'], numberOfRadioButtons=2, sl=1,
    cc1 = 'defaulttread()', cc2 = 'picktread()', en=False)

    makewindow.ObjText=cmds.textFieldButtonGrp(bl="Pick Tread OBJ",bc="PickingObject()",ed=False, en=False)
    makewindow.CopyNum=cmds.intSliderGrp(min=10,v=25,cc="numChange()",f=True, en=False)
    
    cmds.rowLayout( numberOfColumns=2, columnWidth2=(250,250), adjustableColumn=2, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0)] )
    makewindow.makeTread=cmds.button(l="MakeTread",c="MakeTankTread()", en=False)
    makewindow.updatetreadpeice=cmds.button(l="Update Tread Piece",c="updateTread()", en=False)
    
    cmds.setParent(mainCL)
    cmds.separator(w=500)
    
    #Finalize and Reset
    cmds.text(l="")
    cmds.rowLayout( numberOfColumns=2, columnWidth2=(250,250), adjustableColumn=2, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0)] )
    makewindow.FinalizeThread=cmds.button(l="Finalize Tread",c="FinThread()", en=False, h=40, bgc=[0,0.7,0])
    makewindow.ResetBTN=cmds.button(l="Reset All",c="resetAll()",en=False, h=40, bgc=[0.7,0,0])
    cmds.showWindow()


#1 ask user to ensure their tank tread objects are along Z axis
confirm=cmds.confirmDialog(t="Headsup", m="ensure your model is placed along Z axis", b=['Yes','No'], cb='No')
if confirm=='No':
    cmds.confirmDialog(m="well you must set it that way before proceeding")
else:
    makewindow()
    

#start of all functions
def initFunc():


    global change_tread
    global defobj
    global tread_num
    defobj = True
    change_tread = False
    tread_num = objnamer()
    cmds.spaceLocator(n="CircleLocFront")
    cmds.scale(5,5,5)
    cmds.move(0,0,15)
    cmds.setAttr("CircleLocFront.translateX", lock=True)
    cmds.setAttr("CircleLocFront.translateY", lock=True)

    cmds.spaceLocator(n="CircleLocBack")
    cmds.setAttr("CircleLocBack.translateX", lock=True)
    cmds.setAttr("CircleLocBack.translateY", lock=True)
    cmds.scale(5,5,5)
    cmds.move(0,0,-15)

    #we are grouping the locators for easier access and alignment
    cmds.group("CircleLocFront","CircleLocBack",n="LocGRP")

    cmds.confirmDialog(m="now you have 2 locators. Place them at the two ends of your tread at z-axis")
    cmds.button(makewindow.initButton,edit=True,en=False)
    cmds.button(makewindow.MakeCurveBTN,edit=True,en=True)
    cmds.button(makewindow.ResetBTN,edit=True, en=True)
    cmds.frameLayout(makewindow.uiInitFrame, e=True, en=False)
    cmds.frameLayout(makewindow.uiCurveFrame, e=True, en=True)

def resetAll():
    global tread_num

    cmds.button(makewindow.initButton,edit=True,en=True)
    cmds.button(makewindow.MakeCurveBTN,edit=True,en=False)
    cmds.button(makewindow.ResetBTN,edit=True,en=False)
    cmds.button(makewindow.makeTread,edit=True, en=False)
    try:
        cmds.delete("LocGRP")
        cmds.delete("TreadCurve"+str(tread_num))
        try:
            cmds.delete("DefaultTread1")
            cmds.delete("DefaultTread1Group")
        except:
            cmds.delete(selectedOBJ[0]+"Group")
    except:
        pass
    printall()
    flush_cache()


def MakeCurve():
    global tread_curve
    global tread_num
    #here we take the distance of the two locators 
    FrontLocPosZ=cmds.getAttr("CircleLocFront.translateZ")
    BackLocPosZ=cmds.getAttr("CircleLocBack.translateZ")

    FrontLocPosX = cmds.getAttr("CircleLocFront.translateX")
    FrontLocPosY = cmds.getAttr("CircleLocFront.translateY")
    FrontLocPosZ = cmds.getAttr("CircleLocFront.translateZ")
    BackLocPosX = cmds.getAttr("CircleLocBack.translateX")
    BackLocPosY = cmds.getAttr("CircleLocBack.translateY")
    BackLocPosZ = cmds.getAttr("CircleLocBack.translateZ")

    x = math.pow(FrontLocPosX - BackLocPosX, 2)
    y = math.pow(FrontLocPosY - BackLocPosY, 2)
    z = math.pow(FrontLocPosZ - BackLocPosZ, 2)
    vector_distnace = math.sqrt(x + y + z)

    CurveCenter = vector_distnace / 2
    cmds.select("LocGRP")
    cmds.CenterPivot()
    tread_curve = cmds.circle(n="TreadCurve"+str(tread_num),r=CurveCenter,nr=(1,0,0))
    cmds.select(tread_curve,r=True)
    cmds.select("LocGRP",add=True)
    cmds.align(z="mid", atl=True)
    cmds.select(tread_curve,r=True)
    #cmds.FreezeTransformations()
    
    cmds.button(makewindow.MakeCurveBTN,edit=True,en=False)
    cmds.radioButtonGrp(makewindow.peicesel,edit=True, en=True)
    cmds.button(makewindow.makeTread,edit=True, en=True)
    cmds.frameLayout(makewindow.uiCurveFrame, e=True, en=False)
    cmds.frameLayout(makewindow.uiCreateFrame, e=True, en=True)
    
def PickingObject():
    global selectedOBJ
    global updateCopyNum
    global oldobj
    global change_tread
    
    selnum = len(cmds.ls(sl=True))
    obj = cmds.ls(sl=True)[0]
    obj_type = cmds.ls(obj[0:-1]+"Shape"+obj[-1], type='geometryShape', showType=True)

    if selnum == 1 and len(obj_type) == 2 and obj_type[1] == "mesh":
        if change_tread:
            oldobj = selectedOBJ
            # print("oldobj updated ", oldobj)
            cmds.button(makewindow.updatetreadpeice,edit=True, en=True)
        else:
            oldobj = None
            # print("oldobj updated ", oldobj)
            cmds.button(makewindow.makeTread,edit=True, en=True)
            cmds.button(makewindow.updatetreadpeice,edit=True, en=False)
        updateCopyNum = cmds.intSliderGrp(makewindow.CopyNum, q = True, v = True)
        selectedOBJ=cmds.ls(sl=True,o=True)
        # print (selectedOBJ[0])
        cmds.textFieldButtonGrp(makewindow.ObjText,e=True,tx=selectedOBJ[0])
        
        cmds.intSliderGrp(makewindow.CopyNum, edit=True, en=False)
       
    elif selnum !=1:
        cmds.confirmDialog(m="Select 1 object. Currently %s objects are selected" %str(selnum))
        
    elif len(obj_type) !=1 and obj_type == []:
        cmds.confirmDialog(m="You have not selected a mesh type object. Select a mesh type object instead.")
        
        return selectedOBJ
        
def defaulttread():
    global defobj
    defobj = True
    cmds.textFieldButtonGrp(makewindow.ObjText, edit=True, en=False)
    cmds.intSliderGrp(makewindow.CopyNum, e = True, en=False)
    
    if change_tread:
        cmds.button(makewindow.makeTread,edit=True, en=False)
        cmds.button(makewindow.updatetreadpeice,edit=True, en=True)
    else:
        cmds.button(makewindow.makeTread,edit=True, en=True)
        cmds.button(makewindow.updatetreadpeice,edit=True, en=False)
    
def picktread():
    global defobj
    defobj = False
    cmds.textFieldButtonGrp(makewindow.ObjText, edit=True, en=True)
    cmds.button(makewindow.makeTread,edit=True, en=False)
    cmds.intSliderGrp(makewindow.CopyNum, e = True, en=False)
    cmds.button(makewindow.updatetreadpeice,edit=True, en=False)
     
def numChange():
    global defobj
    global updateCopyNum
    global oldobj
    updateCopyNum=cmds.intSliderGrp(makewindow.CopyNum,q=True,v=True)
    # print ("current number is: %s" %updateCopyNum)
    # print(oldobj)
    # print(selectedOBJ)
    if defobj == True:
        try:
            cmds.delete(selectedOBJ)
        except:
            pass
    cmds.delete(selectedOBJ[0]+"Group")
    MakeTankTread()
    return updateCopyNum

def updateTread():
    global updateCopyNum
    global oldobj
    global defobj
    cmds.intSliderGrp(makewindow.CopyNum, e = True, en=True)
    updateCopyNum=cmds.intSliderGrp(makewindow.CopyNum,q=True,v=True)
    cmds.button(makewindow.updatetreadpeice,edit=True, en=False)
    # print ("current number is: %s" %updateCopyNum)
    # print(oldobj)
    # print(selectedOBJ)
    if defobj:
        cmds.delete(selectedOBJ[0]+"Group")
    else:
        cmds.delete(oldobj[0]+"Group")
    MakeTankTread()
    try:
        cmds.delete("DefaultTread1")
    except:
        pass
    return updateCopyNum

def MakeTankTread():
    global updateCopyNum
    global change_tread
    global defobj
    global selectedOBJ
    global proxy_created

    if defobj: # and not proxy_created:
        MakeProxyGeo()
    #     proxy_created = True
    # get original position of the proxy
    originalpos = cmds.getAttr(selectedOBJ[0]+'.translate')[0]

    #step1 animate selected object along the curve
    cmds.select(selectedOBJ,r=True)
    cmds.select(tread_curve,add=True)
    # print(selectedOBJ)
    # print(cmds.ls(sl=True))
    cmds.pathAnimation(fm=True,f=True,fa="z",ua="y",wut="vector",wu=(0,1,0),inverseFront=False,iu=False,b=False,stu=1,etu=updateCopyNum)
    cmds.select(selectedOBJ,r=True)
    cmds.selectKey('motionPath1_uValue',time=(1,updateCopyNum))
    cmds.keyTangent(itt="linear",ott="linear")
    cmds.snapshot(n=selectedOBJ[0],i=1,ch=False,st=1,et=updateCopyNum,u="animCurve")
    cmds.DeleteMotionPaths()

    #send only user's proxy back to its original position
    if selectedOBJ[0] != "DefaultTread1":
        cmds.setAttr(selectedOBJ[0]+'.translate', originalpos[0], originalpos[1], originalpos[2], type="double3")
        newloc = cmds.getAttr(selectedOBJ[0]+'.translate')[0]
        print(newloc)

    cmds.button(makewindow.FinalizeThread,edit=True, en=True)
    cmds.button(makewindow.makeTread,edit=True, en=False)
    cmds.button(makewindow.makeTread,edit=True, en=False)
    cmds.intSliderGrp(makewindow.CopyNum, e = True, en=True)

    change_tread = True
    
def FinThread():
    #now we combine all objects of snapshot and delete the snapshot node
    global tread_num

    cmds.select(selectedOBJ[0]+"Group",r=True)
    tread_full_mesh = cmds.polyUnite(n="TreadFull"+str(tread_num),ch=False)
    cmds.CenterPivot("TreadFull"+str(tread_num))
    cmds.delete(selectedOBJ[0]+"Group")
    cmds.delete("LocGRP")
    # here we create a wite deformer function
    def createWireD(geo,wireCRV,dropoffDist=40.0):
        wire=cmds.wire(geo,w=wireCRV,n='_wire')
        wirenode=wire[0]
        cmds.setAttr(wirenode+'.dropoffDistance[0]',dropoffDist)
    
    cmds.select(tread_full_mesh)
    wireOBJ = cmds.ls(sl=True, o=True)[0]
    print(tread_curve)
    cmds.select(tread_curve)
    print(tread_curve)
    wire_curve = cmds.ls(sl=True,o=True)[0]
    createWireD(wireOBJ, wire_curve,40)
    cmds.select("{}BaseWire".format(tread_curve[0]))
    base_wire_curve = cmds.ls(sl=True,o=True)[0]

    # Grouping all finalized curves and meshs
    cmds.group(wire_curve, wireOBJ, base_wire_curve, n="Tread_#")

    #delete only if its the default tread peice, we make it again in every run
    if selectedOBJ[0] == "DefaultTread1":
        cmds.select(selectedOBJ,r=True)
        cmds.delete()
    else:
        pass
    # flush out all variable in memory
    flush_cache()
    printall()
    
def MakeProxyGeo():
    global selectedOBJ
    global oldobj

    try:
        cmds.delete(oldobj[0]+"Group")
    except:
        pass

    DefaultTread = cmds.polyCube(n="DefaultTread#", w=2, d=2, h=1, sx=6, sy=2, sz=1, ax=(0, 1, 0), cuv=4, ch=1)
    cmds.select(DefaultTread, r=True)
    #selectedOBJ = cmds.ls(sl=True, o=True)
    
    if oldobj == None and selectedOBJ != None:
        oldobj = selectedOBJ
        print("oldobj updated ", oldobj)
    
    selectedOBJ = cmds.ls(sl=True, o=True)
    cmds.scale(2.5, 1, 1)
    # Hard coded faces for extrude
    face_list = ['DefaultTread1.f[1]', 'DefaultTread1.f[4]', 'DefaultTread1.f[7]', 'DefaultTread1.f[10]', 'DefaultTread1.f[18]',
                 'DefaultTread1.f[20:21]', 'DefaultTread1.f[23:24]', 'DefaultTread1.f[26:27]', 'DefaultTread1.f[29]']

    # replace DefaultTread1 with DefaultTread2 when there is more than 1 Tread is created
    new_face_list = []
    for face in face_list:
        new_face_list.append(face.replace("DefaultTread1", selectedOBJ[0]))
    cmds.select(new_face_list)
    cmds.polyExtrudeFacet(new_face_list, ltz=0.8)

    # cleanup for proxy geo
    cmds.select(DefaultTread, r=True)
    cmds.FreezeTransformations()
    cmds.xform(DefaultTread)
    cmds.select(cl=True)

def objnamer():
    tread_num = 1
    while cmds.objExists('Tread_' + str(tread_num)):
        tread_num += 1
    return tread_num

def flush_cache():
    global updateCopyNum
    global selectedOBJ
    global oldobj
    global defobj
    global change_tread
    global tread_curve
    global proxy_created
    updateCopyNum = 25
    defobj = True
    change_tread = False
    # selectedOBJ = None
    oldobj = None
    tread_curve = []
    proxy_created = False

    #Disable everything
    cmds.button(makewindow.FinalizeThread,edit=True, en=False)
    cmds.button(makewindow.initButton, edit=True, en=True)
    cmds.button(makewindow.ResetBTN,edit=True, en=False)
    cmds.intSliderGrp(makewindow.CopyNum, edit=True, en=False)
    cmds.button(makewindow.updatetreadpeice,edit=True, en=False)
    cmds.textFieldButtonGrp(makewindow.ObjText, edit=True, en=False)
    cmds.radioButtonGrp(makewindow.peicesel,edit=True, sl=1, en=False)
    cmds.frameLayout(makewindow.uiCurveFrame, e=True, en=False)
    cmds.frameLayout(makewindow.uiCreateFrame, e=True, en=False)
    cmds.frameLayout(makewindow.uiInitFrame, e=True, en=True)

def printall():
    global updateCopyNum
    global selectedOBJ
    global oldobj
    global defobj
    global change_tread
    global tread_curve
    print("updateCopyNum: ", updateCopyNum)
    print("selectedOBJ: ", selectedOBJ)
    print("oldobj: ", oldobj)
    print("defobj: ", defobj)
    print("change_tread: ", change_tread)
    print("tread_curve: ", tread_curve)