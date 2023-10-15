# Menu Parameter Scroller
#   Menu item cycler & saver
#   Created by Kevin Edzenga, 2023
#
#   Initially created to cycle Fonts faster,
#     And allow saving of the fonts I liked for later comparing
#   Overly commented for learning needs

# -- -- --
# This script is intended to be ran as a shelf tool in Houdini
# -- -- --

# The menu parameter's name
# ( On "Font" nodes, "file" is the font name parameter )
menuParmName = "file"

# The saved menu item parameter's name
savesParmName = "saves"

# When ran on a selected node with the variable "menuParmName" menu parameter,
#   It will change to the next available menu item choice

# When -Control- is held on keyboard,
#   It chooses the prior menu item, going in reverse

# When -Shift- is held on keyboard,
#   A parameter with the variable "savesParmName" is created, if needed.
#   The current menu item select is then added to the "savesParmName" parameter
#     (Checking for duplicate listings too)

# When -Alt- is held on keyboard,
#   It cycles the "savesParmName" parameter list instead of the menu
#   Holding -Control- reverses in the saves list as well

# -- -- -- -- -- -- -- -- -- -- -- --
# -- -- -- -- -- -- -- -- -- -- -- -- --
# -- -- -- -- -- -- -- -- -- -- -- -- -- --

def iterStepSaveFont():
    sel = hou.selectedNodes()
    if len(sel)==0 :
        print( "Warning : Please select a Font sop node first" )
        return; # Exit script
        
    curSel = sel[0] # Can be set up as for loop
        
    # If shift is pressed, save the current name to a Saves list
    if kwargs["shiftclick"]:
        # Parameter list of selected node
        tTemplate = curSel.parmTemplateGroup()
        # If "saves" parm doesn't exist, add it above the "file" parm
        if tTemplate.find( savesParmName ) == None :
            tParm = hou.StringParmTemplate( savesParmName, savesParmName.capitalize(), 1 ) # Create parm
            tTemplate.insertBefore( menuParmName, tParm ) # Add it above the menu list parameter
            curSel.setParmTemplateGroup( tTemplate ) # Update node to have the new parm
        
        savesParm = curSel.parm( savesParmName ) # Save list parameter
        # Add current menu item to save list with ',' separating
        savesVal = savesParm.eval() + "," + curSel.parm( menuParmName ).eval()
        # Check for duplicates, remove empty entries, and then list-to-string separated by ','
        savesVal = ",".join( list(filter( None, set(savesVal.split(",")) )) )
        savesParm.set( savesVal ) # Update save list
        return; # Exit script
        
    # Direction to pick next menu item; '1' Next, '-1' Previous
    shift = 1
    # If control is pressed, go backwards
    if kwargs["ctrlclick"]:
        shift = -1
        
    menuParm = curSel.parm( menuParmName ) # Menu List Parameter object
    
    menuList = menuParm.menuItems() # Menu Items List
    curMenuItem = menuParm.eval() # Current menu item selection
    curIndex = 0
    
    # Alt is pressed, scroll "saves" list
    if kwargs["altclick"]:
        isSaved = menuList.index( curMenuItem )
        
        tTemplate = curSel.parmTemplateGroup()
        if tTemplate.find( savesParmName ) == None :
            print( "Warning : There are no saves to be cycled. Shift+Click this tool to make saves." )
            return; # Exit script
        
        # Set "Available Items" to "Saves" list
        menuList = curSel.parm( savesParmName ).eval().split(",")
        
        # Set to selected save list index,
        #   If menu parm is a selected saved item
        #     Otherwise start from the first entry
        if curMenuItem in menuList :
            curIndex = menuList.index( curMenuItem )
        else:
            # If menu item is not in the saves list, start from the first save in list
            curIndex = 0 # Its already 0, but, eh, its a dependency in code
            shift = 0 # Don't move forward or back in list

    else: # -Alt- isn't pressed
        curIndex = menuList.index( curMenuItem ) # Current menu index in Menu Items List
        
    # Wrap around item selections at the menu list's ends
    #   Using Modulus, 3 % 5 = 3, 5 % 5 = 0, -1 % 5 = 4
    curIndex = ( curIndex + shift ) % len( menuList )
    
    curMenuItem = menuList[ curIndex ] # Get new current menu item
    menuParm.set( curMenuItem ) # Set new current menu item

# Ran as a function to "return" or exit the script early
#   This reduces if-else checks
#     Its not needed, but the code looks cleaner to me
iterStepSaveFont()