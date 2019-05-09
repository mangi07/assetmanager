import models
import locations_import
import os
import pandas as pd


    
def get_df(file, sheet):
    df = pd.read_excel(file, sheet_name=sheet, dtype=str)
    return df


asset = models.Asset()
asset.asset_id = "test_asset"
asset.bulk_count = 15

root_loc = models.Location()
root_loc.description = "root location"
root_loc.parent = None

locs_test1 = "North 3-Story Building >> [111, 109, 108: 2], South 3-Story Building >> [305,  304, 303, 204, 105, 101: shared count], Cafeteria Building >> [C101, C103, C105, C106, C104, C107]"
locs_test2 = "Cafeteria Building >> C101 >> C101 north" # should produce 1 location count
locs_test3 = "Cafeteria Building" # should produce 1 location count
locs_test4 = "Cafeteria Building >> Cafeteria >> Cafeteria food service: 7, FLC >> FLC north annexed large storage room: 7, HBC >> HBC reception: 3"

def test_input_string(s, root):
    #print("Input string: " + s)
    root_loc = locations_import.parse_locations(asset, s, root)
    #locations_import.print_locations(root_loc, 0)
    #print("\nLocation Counts: ")
    #print(len(locations_import.location_counts))


# location counts should be 15, 16, 17, and finally 20
# visually inspect for correct location nesting
test_input_string(locs_test1, root_loc)
test_input_string(locs_test2, root_loc)
test_input_string(locs_test3, root_loc)
test_input_string(locs_test4, root_loc)


# check correct location counts for asset
counts = locations_import.location_counts
assert(False not in [count.asset is asset for count in counts])
assert(counts[0].count == 1)
assert(counts[2].count == 2)
assert(counts[4].count == 1)
assert(counts[8].count == 0)
assert(counts[9].count == 1)
assert(counts[14].count == 1) # Cafeteria Building >> C107
assert(counts[15].count == 1) # Cafeteria Building >> C101 >> C101 north
assert(counts[16].count == 1) # Cafeteria Building
assert(counts[17].count == 7) # Cafeteria Building >> Cafeteria >> Cafeteria food service: 7
assert(counts[18].count == 7) # FLC >> FLC north annexed large storage room: 7
assert(counts[19].count == 3) # HBC >> HBC reception: 3




print("########################################################")
locations_import.outer_traverse_db(root_loc, 1)
print("Length of locations: " + str(len(locations_import.locations)))
assert(len(locations_import.locations) == 25) # not including root, but that can be easily added to the list

for loc in locations_import.locations:
    print("\nnext location:")
    print("description: " + loc.description)
    print("id: " + str(loc.id))
    print("parent id: " + str(loc.parent))

"""
df3 = get_df('input/new_cleaning_locations.xlsx', 'new_cleaning')
for index, row in df3.iterrows():
    # ###############################
    # Locations
    # TODO: print out that module's location_counts
    locs_str = row['db_location']
    asset = assets[row['Item Number']]
    root_location = locations_import.parse_locations(asset, locs_str, root_location)
"""