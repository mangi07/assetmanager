#   Format to parse:
#   [North 3-Story Building >> [111, 109, 108], South 3-Story Building >> [305,  304, 303, 204, 105, 101], Cafeteria Building >> [C101, C103, C105, C106, C104, C107] ]
#   [] optional
#   location without ':' defaults to count of 1 for that location, otherwise loc:# --> count is # for that loc
#   ': shared count' --> leave count blank for that location


#import pandas as pd
import re
import models

"""
loc_df = pd.read_excel('input/new_cleaning_locations.xlsx', sheet_name='new_cleaning', dtype=str)


locations = {}
for index, row in loc_df.iterrows():
    print(len(loc_df))
    locs = row['New Area Name']
"""

location_counts = [] # associating assets and locations, with asset count per location
locations = [] # used in insert_sql.py sql insert

def get_count(buff_str):
    s = buff_str.split(':')
    if len(s) == 2 and s[1].strip() != "shared count":
        return s[0].strip(), int(s[1])
    elif len(s) == 2 and s[1].strip() == "shared count":
        return s[0].strip(), 0 # None yet accounted for at this location
    elif len(s) == 1:
        return s[0], 1


# add location
def add_loc_count(asset, loc, count):
    assert(isinstance(asset, models.Asset))
    assert(isinstance(loc, models.Location))
    assert(isinstance(count, int))
    loc_count = models.LocationCount()
    loc_count.asset = asset
    loc_count.location = loc
    loc_count.count = count
    location_counts.append(loc_count)


# add child to curr_loc
def add_buffer(asset, buff, curr_loc):
    buff_str = ''.join(buff).strip()
    buff_str, count = get_count(buff_str)
    if buff_str not in curr_loc.children:
        # add buffer as new location
        loc = models.Location()
        loc.description = buff_str
        loc.parent = curr_loc
        curr_loc.children[buff_str] = loc
        #locations.append(loc)
    else:
        # find buff_str location in parent
        loc = curr_loc.children[buff_str]
    # add loc to location_counts
    add_loc_count(asset, loc, count)


# work in counts
# work in asset-to-location-count associations
def parse_locations(asset, locs_str, root_loc):
    curr_loc = root_loc
    buff = []
    temp_loc = root_loc # location just before entering a set of brackets
    traversing_down = False
    pc = ""
    
    for c in locs_str:
        if c=='[':
            temp_loc = curr_loc
        elif c==']' and len(buff) > 0 and not ''.join(buff).isspace():
            add_buffer(asset, buff, curr_loc)
            # clear buffer and traverse back up to make parent the current location
            buff.clear()
            curr_loc = temp_loc.parent
        elif c==',' and len(buff) > 0 and not ''.join(buff).isspace():
            add_buffer(asset, buff, curr_loc)
            buff.clear()
            if traversing_down:
                curr_loc = temp_loc
                traversing_down = False
        elif c=='>' and pc=='>':
            # introduce child location of current location and switch to the child
            if not traversing_down:
                temp_loc = curr_loc
            traversing_down = True
            buff_str = ''.join(buff).strip()
            loc = None
            if buff_str not in curr_loc.children:
                loc = models.Location()
                loc.description = buff_str
                loc.parent = curr_loc
                curr_loc.children[buff_str] = loc
            else:
                loc = curr_loc.children[buff_str]
            #add_buffer(asset, buff, loc)
            curr_loc = loc
            buff.clear()
        elif c=='>':
            pass
        elif c not in "[],>":
            buff.append(c)
        
        pc = c
    
    # take care of anything left in the buffer outside the for loop by adding it to its parent
    if len(buff) > 0 and not ''.join(buff).strip().isspace():
        add_buffer(asset, buff, curr_loc)
    
    return root_loc


# walk tree to print it out
import copy

def print_locations(parent, level):
    s = ""
    for x in range(0, level):
        s += ">> "
    print(s + parent.description)
    children = copy.deepcopy([v for (k,v) in parent.children.items()]) # put children on stack
    while len(children) > 0:
        child = children.pop()
        print_locations(child, level+1)


# ###########################################
# set up ids and put tree in list for db
class Count:
    def __init__(self, number):
        self.number = number + 1

def traverse_locations_for_db(parent, count):
    children = copy.deepcopy([v for (k,v) in parent.children.items()]) # put children on stack
    while len(children) > 0:
        child = children.pop()
        child.id = count.number
        child.parent = parent.id
        locations.append(child)
        
        count.number = count.number + 1
        traverse_locations_for_db(child, count)

def outer_traverse_db(root, root_id):
    traverse_locations_for_db(root, Count(root_id))
