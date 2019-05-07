import load_excell as imports
import models
import sqlite3
import sys # for sys.exit()


def insert_message(table, statement):
    print("\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~~~~~~inserting into {}...\n\n".format(table) + statement)


def list_to_column_names(mlist):
    return str(mlist).replace("'",'').replace("[",'').replace("]",'')


def insert_from_lists(mlists, column_names, mtable, mcursor):
    columns_str = list_to_column_names(column_names)
    
    params = "(" + ''.join( ["?, "]*(len(mlists[0])-1) ) + "?)"
    insert = "INSERT INTO {} ({}) VALUES {}".format(mtable, columns_str, params)
    vals = [tuple(vals_list) for vals_list in mlists]
    
    insert_message(mtable, str(vals))
    
    cursor.executemany(insert, vals);
    conn.commit()


def set_ids(items_list):
    index = 1
    for item in items_list:
        item.id = index
        index += 1


def insert_items(table_name, items, clazz, cursor):
    set_ids(items)
    mlists = [item.list_vals() for item in items]
    for mlist in mlists:
        mlist = [None if x=="nan" else x for x in mlists]
        #print(mlists)
    column_names = clazz.list_column_names()
    insert_from_lists(mlists, column_names, table_name, cursor)


conn = sqlite3.connect('assetsdb.sqlite3')
cursor = conn.cursor()

# done, so commented out
#insert_items("manufacturer", imports.manufacturers.values(), models.Manufacturer, cursor)
#insert_items("supplier", imports.suppliers.values(), models.Supplier, cursor)
#insert_items("category", imports.categories.values(), models.Category, cursor)
#insert_items("department", imports.departments.values(), models.Department, cursor)
#insert_items("purchase_order", imports.purchase_orders.values(), models.PurchaseOrder, cursor)

# now we can insert assets that have foreign keys to the items we just inserted above
assets_list = imports.assets.values()
def set_key(asset_field, lookup):
    if asset_field in lookup:
        asset_field = lookup[asset_field].id
# set foreign keys
for asset in assets_list:
    # requisition
    if asset.requisition == "awaiting invoice":
        asset.requisition = 1
    elif asset.requisition == "partial payment":
        asset.requisition = 2
    elif asset.requisition == "paid in full":
        asset.requisition = 3
    elif asset.requisition == "donated":
        asset.requisition = 4
    else:
        asset.requisition = "NULL"
    # receiving
    if asset.receiving == "shipped":
        asset.receiving = 1
    elif asset.receiving == "received":
        asset.receiving = 2
    elif asset.receiving == "placed":
        asset.receiving = 3
    else:
        asset.receiving = "NULL"
    # others
    set_key(asset.po_number, imports.purchase_orders)
    set_key(asset.asset_class1, imports.categories)
    set_key(asset.asset_class1, imports.categories)
    set_key(asset.manufacturer, imports.manufacturers)
    set_key(asset.supplier, imports.suppliers)
    set_key(asset.department, imports.departments)
    
insert_items("asset", imports.assets.values(), models.Asset, cursor)



conn.close()



# ##################################################################################################
# TEST asset results
#for k,v in imports.assets.items():
#    print("\n################################################################")
#    print(v)

# TEST account results
#for k,v in accounts.items():
#    print(v)

# TEST far results
#for k,v in fars.items():
#    print(v)
    
#print("Number of far entries: " + str(len(fars))) # expected: 76 unique entries

# TEST asset-far associations
#for af in asset_fars:
#    print(af)

# TEST asset-picture associations
#for ap in asset_pics:
#    print(ap)

# TEST asset-invoice associations
#for ai in asset_invoices:
#    print(ai)

# TEST locations
#locations_import.print_locations(root_location, 0)
#for loc_count in locations_import.location_counts:
#    if loc_count.asset.bulk_count is not None:
#        print("\n#################################")
#        print(str(loc_count))


"""
assets = {}
todo_account # any items linked to this account may need to be added to FAR
todo_far # any items lnkted to this far may need to be added to FAR
fars = {"TODO":todo_far} # key is acct:pdf (format: ######:#[#[#]]) # TODO
accounts = {"TODO":todo_account} # TODO
asset_fars = [] # TODO
pictures = {}
asset_pics = []
invoices = {}
asset_invoices = []
root_location
"""


