###########################
#  STAMPS SCRIPT
#  version 1.0.0
#  28 April 2022
#  damienengland.com.au
###########################

# Import Modules
import nuke
import random


# CREATE CHILD NODE
def create_stamp(parent):

    parent_name = parent.knob('name').value()
    p_xpos = parent.xpos()
    p_ypos = parent.ypos()

    stamp_name = f"{parent_name}_{random.randint(0,100000)}"

    stamp = nuke.createNode('NoOp', inpanel=False)
    stamp['tile_color'].setValue(0x20101ff)
    stamp.setInput(0, nuke.toNode(parent_name))
    stamp['hide_input'].setValue(True)
    stamp['xpos'].setValue(p_xpos)
    stamp['ypos'].setValue(p_ypos + 50)
    stamp['name'].setValue(stamp_name)
    stamp['label'].setValue("test")

    stamp_tab = nuke.Tab_Knob('stamp', 'Stamp')
    stamp.addKnob(stamp_tab)
    parent_id = nuke.String_Knob('parent_id', 'Parent ID', parent_name)
    st_divider = nuke.Text_Knob("divider", "")
    stamp.addKnob(parent_id)
    stamp.addKnob(st_divider)

    auto_label = "nuke.thisNode().knob('parent_id').value()"
    stamp['autolabel'].setValue(auto_label)

    # ADD STAMP TO PARENT STAMP LIST
    current_stamp_list = parent.knob("stamp_list").value()
    new_stamp_list = current_stamp_list + f"{stamp.knob('name').value()}\n"
    parent.knob("stamp_list").setValue(new_stamp_list)

    # CONNECT CHILD TO PARENT IF DISCONNECTED
    RECONNECT = "reconnect_parent(nuke.thisNode())"
    reconnect_btn = nuke.PyScript_Knob('reconnect', 'Reconnect', RECONNECT)
    reconnect_btn.setFlag(nuke.STARTLINE)
    stamp.addKnob(reconnect_btn)


def reconnect_all_stamps(parent):
    stamps = parent.knob("stamp_list").value()
    stamp_list = stamps.replace("\n", ".").split(".")[:-1:]

    new_list = ""
    for stamp in stamp_list:
        node = nuke.toNode(stamp)
        if node is not None:
            new_list += f"{stamp}\n"
            reconnect_parent(node)
            node.setSelected(True)

    parent.knob("stamp_list").setValue(new_list)


# SELECT ALL STAMPS FROM LIST
def select_stamps(parent):
    stamps = parent.knob("stamp_list").value()
    stamp_list = stamps.replace("\n", ".").split(".")[:-1:]
    for stamp in stamp_list:
        nuke.toNode(stamp).setSelected(True)


# CONNECT CHILD TO PARENT
def reconnect_parent(stamp):

    parent_name = stamp['parent_id'].value()
    parent_node = nuke.toNode(parent_name)

    if parent_node is None:
        nuke.message('ERROR: Unable to locate parent!')
        return

    stamp.setInput(0, parent_node)


# UPDATE PARENT LABEL
def update_label(node):
    node["name"].setValue(node["parent_label"].value())


# MAIN TOOL FUNCTION
def create_parent():

    # CREATE PARENT
    txt = nuke.getInput('Stamp Title')
    if txt is None:
        return
    else:
        p_label = txt

    parent = nuke.createNode('NoOp')
    parent['name'].setValue(p_label)

    # PARENT TAB KNOBS AND BUTTONS
    parent_tab = nuke.Tab_Knob('stamp_parent', 'Stamp Parent')
    parent.addKnob(parent_tab)
    parent_label_string_knob = nuke.String_Knob('parent_label', 'Title:', p_label)
    parent.addKnob(parent_label_string_knob)

    # UPDATE LABEL
    UPDATE_LABEL_PYSCRIPT = "update_label(nuke.thisNode())"
    p_update_label = nuke.PyScript_Knob('update_label', 'Update Label', UPDATE_LABEL_PYSCRIPT)
    parent.addKnob(p_update_label)

    # DIVIDER
    p_divider = nuke.Text_Knob("divider", "")
    parent.addKnob(p_divider)

    # DESCRIPTOR
    p_descriptor = nuke.Text_Knob("", "Stamps:", " ")
    parent.addKnob(p_descriptor)

    # CREATE STAMP
    CREATE_STAMP_PYSCRIPT = "create_stamp(nuke.thisNode())"
    p_create_stamp_btn = nuke.PyScript_Knob('create_stamp', 'Create Stamp', CREATE_STAMP_PYSCRIPT)
    parent.addKnob(p_create_stamp_btn)

    # SELECT STAMPS
    SELECT_STAMPS_PYSCRIPT = "select_stamps(nuke.thisNode())"
    p_select_stamps_btn = nuke.PyScript_Knob("select_stamps", "Select Stamps", SELECT_STAMPS_PYSCRIPT)
    parent.addKnob(p_select_stamps_btn)

    # STAMPS LIST TAB
    stamp_list_tab = nuke.Tab_Knob("stamps", "Stamps")
    parent.addKnob(stamp_list_tab)
    stamp_list_knob = nuke.Multiline_Eval_String_Knob('stamp_list', 'Stamp Nodes', '')
    parent.addKnob(stamp_list_knob)

    # UPDATE STAMPS FROM LIST
    RECONNECT_ALL_STAMPS_PYSCRIPT = "reconnect_all_stamps(nuke.thisNode())"

    update_stamp_list_btn = nuke.PyScript_Knob('reconnect_all_stamps', 'Reconnect Stamps', RECONNECT_ALL_STAMPS_PYSCRIPT)
    update_stamp_list_btn.setFlag(nuke.STARTLINE)
    parent.addKnob(update_stamp_list_btn)

    # SET DEFAULT TAB
    parent.knob("stamp_parent").setFlag(0)

