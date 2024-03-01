import maya.cmds as cmds
import time

from functions.ChainMaker.ui_utils import enable_radio_btn

message = "hello"
enable_radio_btn(message)

class CurveRigAnimChainTool:
    def __init__(self):
        self.isFirstTime = True
        self.ChainCount = 22
        self.selected_curve_name = ""
        self.curve_type = 3
        self.first_time_make_chain = True
        self.proxy_geo = None
        self.mesh_selected = None
        self.user_selected_mesh = None

        # let's create a window and UI
        win_name = "Rebuilder"

        if cmds.window(win_name, q=True, ex=True):
            cmds.deleteUI(win_name)

        cmds.window(win_name, t="Curve Rigger", w=700, h=450, s=False)
        cmds.columnLayout(margins=5)
        master_layout = cmds.columnLayout(mar=5)
        cmds.rowColumnLayout(numberOfColumns=1)
        cmds.text("Curve Rigger Tool", font="boldLabelFont")
        cmds.separator(w=700, h=10)
        cmds.setParent(master_layout)

        # *****************************************************************************************************************
        self.ui_curve_frame = cmds.frameLayout(l="Curve Settings", w=700, cll=True, cl=False)
        self.ui_curve_layout = cmds.columnLayout()
        cmds.text("Before anything, ensure you have a curve selected to restructure the curve use this slider")
        cmds.setParent(self.ui_curve_layout)
        scroll_layout = cmds.rowLayout(numberOfColumns=2)
        text_scroll_layout = cmds.scrollLayout(w=250, h=50, hst=0, vst=16)

        if self.find_object_in_scene()[0]:
            self.curve_scroll_list = cmds.textScrollList(parent=text_scroll_layout,
                                                         numberOfRows=self.find_object_in_scene()[1],
                                                         allowMultiSelection=True,
                                                         append=self.find_object_in_scene()[0],
                                                         sc="ui_utils.enable_radio_btn(self.curve_type)"
                                                         )
            cmds.setParent(scroll_layout)
            self.btn_refresh = cmds.iconTextButton(style='iconAndTextVertical',
                                                   image1='refresh.xpm',
                                                   label='refresh',
                                                   al="right",
                                                   c="self.refresh_list()"
                                                   )

            cmds.setParent(scroll_layout)
            cmds.setParent(self.ui_curve_layout)

            self.curve_type = cmds.radioButtonGrp(label='Type of Curve',
                                                  labelArray4=['Linear-1', 'Quadratic-2', 'Cubic-3', 'Quintic-5'],
                                                  numberOfRadioButtons=4,
                                                  cc1='self.get_curve_type()',
                                                  cc2='self.get_curve_type()',
                                                  cc3='self.get_curve_type()',
                                                  cc4='self.get_curve_type()',
                                                  en=False
                                                  )

            cmds.rowLayout(numberOfColumns=2)
            self.span_count = cmds.intSliderGrp(min=3, max=100, v=3, cc="self.find_span_count()", f=True, en=False)
            self.cb_adjust_smoothness = cmds.checkBox(l="Adjust Smoothness",
                                                      cc="self.enable_smoothness_slider()",
                                                      en=False)

            cmds.setParent(self.ui_curve_layout)
            cmds.separator(w=700)
            cmds.text("now if you want to smooth it, use this slider to smooth")
            self.SmoothNess = cmds.floatSliderGrp(min=0, max=10, v=0, cc="SmoothChange()", f=True, en=False)
            self.btn_next_to_make_controllers = cmds.button(l="Next", c="expand_controller_section()", en=False)
            cmds.separator(w=700)
            cmds.setParent(master_layout)

            # *****************************************************************************************************************
            self.ui_controller_frame = cmds.frameLayout(l="Controller & Chains", w=700, cll=True, cl=True)
            self.ui_controller_layout = cmds.columnLayout()
            cmds.text("now if you are done with the curve, use this button to create controllers")
            self.RedoCTRL = cmds.intSliderGrp(min=3, max=100, v=3, cc="CTRLRedo()", f=True, en=False)
            cmds.rowLayout(numberOfColumns=3)
            self.btn_cmaker = cmds.button(l="CTRL maker", c="CMaker()", en=False)
            self.btn_to_final_step = cmds.button(l="Next", c="make_chain_section()", en=False)
            self.btn_update = cmds.button(l="Update Chain", c="update_chain()", en=False)
            cmds.setParent(self.ui_controller_layout)
            cmds.separator(w=700)
            cmds.text("now if you are done, select your desired object and click next")
            cmds.setParent(self.ui_controller_layout)
            cmds.rowLayout(numberOfColumns=2)
            # make_window.btn_make_chain_from_selected_obj = cmds.button(l="Make Chain", c="FinalStep()", en=False)
            self.btn_make_chain = cmds.button(l="MakeChain Only", c="MakeChain()", en=False)
            self.cb_make_proxy = cmds.checkBox(l="Use Proxy Geo", cc="make_proxy_geo()", en=False)
            cmds.setParent(self.ui_controller_layout)
            cmds.setParent(master_layout)

            # *****************************************************************************************************************

            cmds.showWindow()
        else:
            cmds.confirmDialog(title='Error', message='You need to create a curve first.', icon='critical')



    # start of the functions
    def get_curve_type(self):
        global curve_type
        ui_utils.enable_button(self.span_count)
        # cmds.intSliderGrp(self.span_count, e=True, en=True)
        cmds.floatSliderGrp(self.SmoothNess, e=True, en=False)
        cmds.checkBox(self.cb_adjust_smoothness, e=True, v=False)
        curve_type = cmds.radioButtonGrp(self.curve_type, q=True, sl=True)
        if curve_type == 1:
            cmds.confirmDialog(m="Linear curves can not be smoothened.")
        print(curve_type)

    def find_span_count(self):
        global isFirstTime
        global selected_curve_name
        global curve_type
        if curve_type == 4:
            curve_type = 5
        if curve_type == 1:
            cmds.checkBox(self.cb_adjust_smoothness, e=True, en=False)
        else:
            cmds.checkBox(self.cb_adjust_smoothness, e=True, en=True)

        if not isFirstTime:
            cmds.undo()

        cmds.radioButtonGrp(self.curve_type, e=True, en=False)
        cmds.textScrollList(self.curve_scroll_list, e=True, en=False)
        cmds.button(self.btn_next_to_make_controllers, e=True, en=True)
        spanValue = cmds.intSliderGrp(self.span_count, q=True, v=True)
        selected_curve_name = cmds.textScrollList(self.curve_scroll_list, q=True, si=True)

        cmds.select(selected_curve_name)
        selectedCurve = cmds.ls(sl=True)
        cmds.rebuildCurve(selectedCurve, rpo=True, kep=True, rt=0, s=spanValue, d=curve_type)
        cmds.select(selectedCurve)
        isFirstTime = False

    def enable_smoothness_slider(self):
        self.isFirstTime = True
        cmds.intSliderGrp(self.span_count, e=True, en=False)
        cmds.floatSliderGrp(self.SmoothNess, e=True, en=True)

    def expand_controller_section(self):
        # Expand toggles
        cmds.frameLayout(self.ui_curve_frame, e=True, cl=True)
        cmds.frameLayout(self.ui_controller_frame, e=True, cl=False)
        # Button enable/disable
        cmds.button(self.btn_next_to_make_controllers, e=True, en=False)
        cmds.button(self.btn_cmaker, e=True, en=True)
        # Checkbox disabled
        cmds.checkBox(self.cb_adjust_smoothness, e=True, en=False)
        # sliders disabled
        cmds.floatSliderGrp(self.SmoothNess, e=True, en=False)
        cmds.intSliderGrp(self.RedoCTRL, e=True, en=False)

    def make_chain_section(self):
        # Expand toggles
        # cmds.frameLayout(make_window.ui_controller_frame, e=True, cl=True)
        cmds.intSliderGrp(self.RedoCTRL, e=True, en=False)
        cmds.button(self.btn_to_final_step, e=True, en=False)
        # cmds.button(make_window.btn_make_chain_from_selected_obj, e=True, en=True)
        cmds.button(self.btn_make_chain, e=True, en=True)
        cmds.checkBox(self.cb_make_proxy, e=True, en=True)

        cmds.confirmDialog(t="Error", m="You should select one mesh!")

    def SmoothChange(self):
        global isFirstTime
        if not isFirstTime:
            cmds.undo()

        cmds.button(self.btn_next_to_make_controllers, e=True, en=True)
        selected_curve_name = cmds.textScrollList(self.curve_scroll_list, q=True, si=True)
        newSmooth = cmds.floatSliderGrp(self.SmoothNess, q=True, v=True)
        selectedCurve = cmds.ls(selected_curve_name, sl=True)
        cmds.smoothCurve(selectedCurve[0] + ".cv[*]", s=newSmooth)
        cmds.select(selectedCurve)
        isFirstTime = False

    def CMaker(self):
        global ChainCount

        cmds.floatSliderGrp(self.SmoothNess, e=True, en=False)
        cmds.intSliderGrp(self.RedoCTRL, e=True, en=False)
        cmds.button(self.btn_to_final_step, e=True, en=True)

        selectedCRV = cmds.ls(sl=True)
        EPlist = cmds.ls(selectedCRV[0] + ".ep[*]", fl=True)
        ChainCount = len(EPlist)
        locList = []
        # now with having those two lists we can create locators and dump them on each point in order
        for EPi in EPlist:
            cmds.select(EPi, r=True)
            cmds.pointCurveConstraint()
            cmds.CenterPivot()
            locList.append(cmds.rename("EPCTRL1"))
        cmds.select(locList)
        cmds.group(n="AllLocators")
        cmds.select(selectedCRV)
        cmds.select(cl=True)
        cmds.intSliderGrp(self.RedoCTRL, e=True, en=True)
        cmds.button(self.btn_cmaker, e=True, en=False)

    def CTRLRedo(self):
        global selected_curve_name

        try:
            cmds.delete("AllLocators")
        except:
            pass
        newRespan = cmds.intSliderGrp(self.RedoCTRL, q=True, v=True)
        cmds.select(selected_curve_name)
        selectedcurve = cmds.ls(sl=True)

        cmds.rebuildCurve(selectedcurve, rpo=True, kep=True, rt=0, s=newRespan)
        cmds.select(selectedcurve)
        self.CMaker()

    def update_chain(self):
        global proxy_geo, mesh_selected, user_selected_mesh

        cmds.button(self.btn_to_final_step, e=True, en=False)
        try:
            cmds.delete("AllLinks")
            cmds.select(user_selected_mesh)
        except:
            pass

        cmds.delete(mp=True)

        if user_selected_mesh == proxy_geo:
            cmds.select(proxy_geo)
            cmds.setAttr(proxy_geo[0] + ".translateX", 0.0)
            cmds.setAttr(proxy_geo[0] + ".translateY", 0.0)
            cmds.setAttr(proxy_geo[0] + ".translateZ", 0.0)
            cmds.setAttr(proxy_geo[0] + ".rotateX", 0.0)
            cmds.setAttr(proxy_geo[0] + ".rotateY", 0.0)
            cmds.setAttr(proxy_geo[0] + ".rotateZ", 0.0)

        self.CTRLRedo()

        cmds.select(user_selected_mesh)

        self.MakeChain()

    def scale_chain(self, scale_value):
        Clink_lists = cmds.ls("CLink*", fl=True, type="transform")
        for i in Clink_lists:
            cmds.setAttr("{}.scaleX".format(i), scale_value)
            cmds.setAttr("{}.scaleY".format(i), scale_value)
            cmds.setAttr("{}.scaleZ".format(i), scale_value)

    def MakeChain(self):
        global ChainCount, selected_curve_name, first_time_make_chain, mesh_selected, user_selected_mesh

        user_selected_mesh = cmds.ls(sl=True)
        cmds.button(self.btn_to_final_step, e=True, en=False)
        # mesh_selected = len(cmds.ls(sl=True))
        # obj = cmds.ls(sl=True)[0]
        # obj_type = cmds.ls(obj[0:-1] + "Shape" + obj[-1], type='geometryShape', showType=True)

        # if mesh_selected == 1 and obj_type[1] == "mesh":
        if user_selected_mesh:

            cmds.button(self.btn_update, e=True, en=True)

            selected_curve_name = cmds.textScrollList(self.curve_scroll_list, q=True, si=True)
            selectedOBJ = cmds.ls(sl=True)
            cmds.select(selectedOBJ, r=True)
            cmds.select(selected_curve_name, add=True)
            cmds.pathAnimation(fm=True, f=True, fa="x", ua="y", wut="vector", wu=(0, 1, 0), inverseFront=False,
                               iu=False,
                               b=False, stu=1, etu=ChainCount)
            cmds.select(selectedOBJ, r=True)

            AnimCTList = cmds.ls("EPCTRL*", tr=True)
            cmds.selectKey('motionPath1_uValue', time=(1, ChainCount))
            cmds.keyTangent(itt="linear", ott="linear")
            chainLinks = []

            for curkey in range(1, ChainCount + 1):
                cmds.currentTime(curkey)
                cmds.select(selectedOBJ, r=True)
                cmds.FreezeTransformations()
                cmds.duplicate()
                cmds.select(AnimCTList[curkey - 1], add=True)
                cmds.parentConstraint(w=1.0)
                chainLinks.append(cmds.rename("CLink1"))

            cmds.select(chainLinks)
            cmds.group(n="AllLinks")
            linksCount = len(chainLinks)

            for i in range(1, linksCount, 2):
                cmds.currentTime(i)
                cmds.select(chainLinks[i])
                cmds.setAttr(chainLinks[i] + ".rx", 90)
            cmds.DeleteMotionPaths()

            first_time_make_chain = False
            cmds.button(self.btn_make_chain, e=True, en=False)
            cmds.intSliderGrp(self.RedoCTRL, e=True, en=True)
            cmds.checkBox(self.cb_make_proxy, e=True, en=False)

            self.scale_chain(10)

    def make_proxy_geo(self):
        global proxy_geo

        proxy_geo = cmds.polyTorus(n="ProxyGeo", sa=10, sh=10, sr=0.3)
        edges_to_scale = []
        edges_template = ["pTorus1.e[109]", "pTorus1.e[119]", "pTorus1.e[129]", "pTorus1.e[139]", "pTorus1.e[149]",
                          "pTorus1.e[159]", "pTorus1.e[169]", "pTorus1.e[179]", "pTorus1.e[189]", "pTorus1.e[199]",
                          "pTorus1.e[104]", "pTorus1.e[114]", "pTorus1.e[124]", "pTorus1.e[134]", "pTorus1.e[144]",
                          "pTorus1.e[154]", "pTorus1.e[164]", "pTorus1.e[174]", "pTorus1.e[184]", "pTorus1.e[194]"]

        for edge in edges_template:
            suffix_name = edge.split(".")[-1]
            new_edge_name = "ProxyGeo." + str(suffix_name)
            edges_to_scale.append(new_edge_name)

        cmds.select(cl=True)
        cmds.select(edges_to_scale)
        cmds.scale(0.828, 1, 1, )
        cmds.select(proxy_geo)

        cmds.checkBox(self.cb_make_proxy, e=True, en=False)

    def find_object_in_scene(self):
        all_curves = cmds.ls(type="nurbsCurve")
        all_transform_node = []
        number_of_curves = 0
        for curve_shape in all_curves:
            transform_node = cmds.listRelatives(curve_shape, parent=True, fullPath=True)[0]
            transform_node = transform_node.split("|")[-1]
            all_transform_node.append(transform_node)
        number_of_curves = len(all_transform_node)
        return all_transform_node, number_of_curves

    def enable_reconstruct(self):
        cmds.radioButtonGrp(self.curve_type, e=True, en=True)

