# Nuke Stamps
*A simplified version of the widely used nuke plugin know as Stamps Tool. This script allows you to create a node 
within Nuke and create stamps / references to the parent node. This allows for tidier scripts and cleaner workflows.*

##GETTING STARTED
The first thing to do is to locate your .nuke folder. *(It is hidden by default.)*

- **Windows:** C:\ Users\< username >\.nuke
 
- **Mac:** /Users/< username >/.nuke

Look for a menu.py file.

### Installation

1. Paste the below code into the **menu.py** file located in your .nuke directory

```
# Import Custom Modules
from stamps_main import *

m = nuke.menu("Nuke")
m.addCommand("Python Tools/Stamps", "create_parent()", shortcut="F8")
```

2. Paste the below code into the **init.py** file located in your .nuke directory

```
# Make sure you use the correct stamp version
nuke.pluginAddPath('./stamps_1.0.0')
```

3. Place the Stamps_1.0.0 folder into your .nuke directory
4. Restart Nuke and start stamping!

## HOW TO USE
**Create Node**
1. Select a node in your node graph
2. Navigate to the *"Python Tools/Stamp"* menu button at the top of the application or use Hotkey *"F8"*
3. Provide Stamp name

**Create Stamp**
1. Open Properties tab in nuke.
2. Click *Create Stamp* button

**Node Options**

*Update Label:* Updates all linked stamps with the Title input.

*Select Stamps:* Sets each stamp selection as True

*Reconnect Stamps:* Reconnects all stamps in stamp list to parent node


## Requirements
- The Foundry - Nuke Licence


## Contact
#### Damien England
#### damien.england@icloud.com
#### [Website](http://www.damienengland.com.au) 

