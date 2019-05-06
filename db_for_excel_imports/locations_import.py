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

# schema done
# class Asset:
#     id = None
#     asset_id = None # DONE
#     description = None # DONE
#     cost = None # what Harvest paid # DONE
#     cost_brand_new = None # DONE
#     bulk_count = None # often 1 but several entries are bulk # DONE
    
#     def __str__(self):
#         return "Asset ID " + "'"+str(self.asset_id)+"'"


# class Location:
#     def __init__(self):
#         self.id = None
#         self.description = None
#         self.parent = None # reference to other location same table
#         self.children = {}
    
# # schema done
# class LocationCount:
#     id = None
#     asset = None
#     location = None# can be a default location if location is unknown (eg: add missing counts to default location during audit)
#     count = None # how many of that asset at location
#     audit_date = None # date last audited

#############################
# test tree:

locs_test = "[North 3-Story Building >> [111, 109, 108: 2], South 3-Story Building >> [305,  304, 303, 204, 105, 101: shared count], Cafeteria Building >> [C101, C103, C105, C106, C104, C107] ]"
locs_test2 = "[North 3-Story Building >> [111, 109, 108, 107], South 3-Story Building >> [305,  304, 303, 204, 105, 101], Cafeteria Building >> [C101, C103, C105, C106, C104, C107] ]"
# also test with loc:# and loc:shared count (leave count field blank if "shared count")
location_counts = [] # associating assets and locations, with asset count per location


def get_count(buff_str):
    s = buff_str.split(':')
    if len(s) == 2 and s[1].strip() != "shared count":
        return s[0].strip(), int(s[1])
    elif len(s) == 2 and s[1].strip() == "shared count":
        return s[0].strip(), None
    elif len(s) == 1:
        return s[0], 1


def add_loc_count(asset, loc, count):
    loc_count = models.LocationCount()
    loc_count.asset = asset
    loc_count.location = loc
    loc_count.count = count
    location_counts.append(loc_count)


def add_buffer(asset, buff, curr_loc):
    buff_str = ''.join(buff).strip()
    buff_str, count = get_count(buff_str)
    if buff_str not in curr_loc.children:
        # add buffer as new location
        loc = models.Location()
        loc.description = buff_str
        loc.parent = curr_loc
        curr_loc.children[buff_str] = loc
    else:
        # find buff_str location in parent
        loc = curr_loc.children[buff_str]
    # add loc to location_counts
    add_loc_count(asset, loc, count)


# TODO: work in counts
# TODO: work in asset-to-location-count associations
def parse_locations(asset, locs_str, root_loc):
    curr_loc = root_loc
    parent = None
    buff = []
    pc = ""
    
    sc = list("shared count")
    scx = 0 # position in "shared count"
    sc_search = False

    for c in locs_str:
        if c=='[':
            pass
        elif c==']' and len(buff) > 0 and not ''.join(buff).isspace():
            add_buffer(asset, buff, curr_loc)
            # clear buffer and traverse back up to make parent the current location
            buff.clear()
            curr_loc = curr_loc.parent
        elif c==',' and len(buff) > 0 and not ''.join(buff).isspace():
            add_buffer(asset, buff, curr_loc)
            buff.clear()
        elif c=='>' and pc=='>':
            # introduce child location of current location and switch to the child
            buff_str = ''.join(buff).strip()
            loc = None
            if buff_str not in curr_loc.children:
                loc = models.Location()
                loc.description = buff_str
                loc.parent = curr_loc
                curr_loc.children[buff_str] = loc
            else:
                loc = curr_loc.children[buff_str]
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

#parse_locations(asset, locs_test, root_loc)
#parse_locs(asset, locs_test2, root_loc)
#print("okay")



# walk tree to print it out
import copy
#curr = root_loc

def print_locations(parent, level):
    s = ""
    for x in range(0, level):
        s += ">> "
    print(s + parent.description)
    children = copy.deepcopy([v for (k,v) in parent.children.items()]) # put children on stack
    while len(children) > 0:
        child = children.pop()
        print_locations(child, level+1)


