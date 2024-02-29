import maya.cmds as cmds

#Global Variables
loc_trans = []
locator_list = []
ctrl_list = []
jointQVal = 0

# region UI
WND_NAME = "wndArmRig"
WND_WIDTH = 400
UI_WARNING_BGC = [1, 1, 0]

def SetFK(isChecked:bool):
    global isFK 
    isFK = isChecked

if cmds.window(WND_NAME, q=True, exists=True):
    cmds.deleteUI(WND_NAME)
wnd = cmds.window(WND_NAME, t="Arm Rigging Basic Tool", w=WND_WIDTH)

mainCL = cmds.columnLayout()

uiInitFrame = cmds.frameLayout(l="Initialize", w=WND_WIDTH, cll=True)
uiInitCL = cmds.columnLayout()

# cmds.text(l="Requirement!", fn="boldLabelFont", bgc=UI_WARNING_BGC)
cmds.text(l="Please input how many pieces the arm has.")
NumOfP = cmds.intSliderGrp(l="Total Pieces: ", min=2, v=3, field=True)
cmds.separator(h=15)
uiBtnInit = cmds.button(l="Initialize", w=WND_WIDTH/4, c="Initialize()")
cmds.setParent(mainCL)
cmds.separator(h=15)

uiRigFrame = cmds.frameLayout(l="Rig", w=WND_WIDTH, cll=True, en=False)
uiRigCL = cmds.columnLayout()
cmds.text(l="Requirement!", fn="boldLabelFont", bgc=UI_WARNING_BGC)
cmds.text(l="Please position the locators where you want the joints to be created.")
cmds.separator(h=15)

uiFKMenu = cmds.optionMenuGrp(l="FK/IK Mode:")
cmds.menuItem(l="FK")
cmds.menuItem(l="IK")
cmds.separator(h=15)
cmds.button(l="Create Rig", w=WND_WIDTH/4, c="Create()")

cmds.setParent(mainCL)

uiIKFrame = cmds.frameLayout(l="IK Creator", w=WND_WIDTH, cll=True, en=False)
uiIKCL = cmds.columnLayout()

cmds.text(l="Requirement!", fn="boldLabelFont", bgc=UI_WARNING_BGC)
cmds.text(l="Please select start and end joints that you want an IK Handle for, then click \"Create IK\" button.")
cmds.separator(h=15)
cmds.button(l="Create IK Handle", w=WND_WIDTH/4, c="CreateIK()")

cmds.setParent(mainCL)

cmds.separator(h=25)
cmds.text(l="Please select all arm peices and then click \"Finalize\" button.")
cmds.rowLayout(nc=2)
btn_fin = cmds.button(l="Finalize", w=WND_WIDTH/4, c="Finalize()", en=False)
btn_reset = cmds.button(l="Reset", w=WND_WIDTH/4, c="Reset()", en=False)
cmds.showWindow()


#start of functions
def Initialize():
    MakeLoc()
    cmds.frameLayout(uiRigFrame, e=True, en=True)
    cmds.button(btn_reset, e=True, en=True)
    cmds.frameLayout(uiInitFrame, e=True, en=False)

def Create():
    CreateRig()
    mode = cmds.optionMenuGrp(uiFKMenu, q=True, v=True)
    if(mode == "FK"):
        cmds.button(btn_fin, e=True, en=True)
    elif(mode == "IK"):
        cmds.frameLayout(uiIKFrame, e=True, en=True)
    cmds.button(btn_reset, e=True, en=True)
    cmds.frameLayout(uiRigFrame, e=True, en=False)

def CreateIK():
    cmds.button(btn_fin, e=True, en=True)
    CreateIKHandle()
    
def Reset():
    ResetLoc()
    cmds.frameLayout(uiInitFrame, e=True, en=True)
    cmds.frameLayout(uiRigFrame, e=True, en=False)
    cmds.frameLayout(uiIKFrame, e=True, en=False)
    cmds.button(btn_fin, e=True, en=False)
    cmds.button(btn_reset, e=True, en=False)

# endregion

# Start of functions
def MakeLoc():
    global locator_list
    global loc_trans
    global jointQVal
    locator_list=[]
    loc_trans=[]
    jointQVal = cmds.intSliderGrp(NumOfP,q=True,value=True)
    for i in range(1, jointQVal+2):
        newLoc = cmds.spaceLocator(n="Armlocator_{}".format(i), p = (0,0,i*5))
        cmds.scale(3,3,3)
        cmds.CenterPivot()
        locator_list.append(newLoc[0])

def ResetLoc():
    cmds.select(locator_list)
    cmds.delete()
    locator_list.clear()
    cmds.select(joint_list)
    cmds.delete()
    joint_list.clear()
    cmds.select(ctrl_list)
    cmds.delete()
    ctrl_list.clear()


def CreateRig():
    global joint_list, locator_list
    for loc in locator_list:
        print(loc)
        loc_pos = cmds.getAttr(loc+".wp")
        loc_trans.append(loc_pos[0])
    cmds.select(cl=True)
    joint_list = []
    for i in loc_trans: 
        created_joint = cmds.joint(n="ArmJoint_#", p=i)
        joint_list.append(created_joint)

def CreateIKHandle():
    global ctrl_list
    selectedJoint = []
    selectedJoint = cmds.ls(sl=True)
    # Making IK handle
    newIKH = cmds.ikHandle(n="IKCT", sj = selectedJoint[0], ee=selectedJoint[-1], s=False, snc=False)
    new_ctrl = cmds.circle(r=4, nr=(0,1,0))
    cmds.matchTransform(new_ctrl, newIKH, pos=True, rot=True)
    cmds.select(new_ctrl)
    cmds.FreezeTransformations()
    cmds.parentConstraint(new_ctrl, newIKH[0], mo = True)
    ctrl_list.append(new_ctrl[0])

def Finalize():
    global ctrl_list, joint_list, jointQVal
    #ask user to select all arm peices
    if len(cmds.ls(sl=True)) == jointQVal:
    
        # Getting user option of whether use IK or FK 
        user_option = cmds.optionMenuGrp(uiFKMenu, query=True, value=True)
        
        armlist = cmds.ls(sl=True)
        print(armlist)
        cmds.select(cl=True)
        
        new_jnt_list = joint_list.copy()
        new_jnt_list.pop()
        
        cmds.select(new_jnt_list, r=True)
        cmds.select(armlist, add=True)
        cmds.SmoothBindSkin()

        for j in range(len(new_jnt_list)):
            cmds.select(armlist[j], r=True)
            cmds.ConvertSelectionToVertices()
            cmds.skinPercent('skinCluster'+str(j+1), tv=[new_jnt_list[j], 1.0])
        
        # Options for making FK handles
        if user_option == "FK":
                
            ctrl_list = []
            # get rid of the ctrl for end joint
            
            for jnt in new_jnt_list: 
                new_ctrl = cmds.circle(n="{}_ctrl".format(jnt), r=4, nr=(0,1,0))
                cmds.matchTransform(new_ctrl, jnt, pos=True, rot=True)
                cmds.select(new_ctrl)
                cmds.FreezeTransformations()
                cmds.parentConstraint(new_ctrl, jnt, mo = True)
                ctrl_list.append(new_ctrl[0])
            # parent constrainting controls
            numOfCtrl = len(ctrl_list)
            for i in range(numOfCtrl-1):
                print(i)
        
                cmds.parentConstraint(ctrl_list[i],ctrl_list[i+1], mo = True)
            
        joint_list = []
        ctrl_list = []
        Reset()
    else:
        cmds.confirmDialog(t="Error", m="Select all {} arm peices".format(jointQVal))

            
def logger(message, btn_message):
    cmds.confirmDialog(m=message,b=btn_message)
    