# ###################################################################
# File: import.py
# Created: 4/29/2019
#
# Description: python classes here correspond to schema in import.sql
#   Populates data frames with the classes.
#   Uses these classes to populate sqlite db...
#   Or could be used to populate django db
#   once the corresponding models are created.
#
#   Money values are multiplied by 10,000,000,000 for 10 digits of decimal precision
#
#   Warning: Once imported, some values could be 'nan' instead of None, so check for both.
#
#   Relationships referenced in python by object rather than by id as in db.
# ###################################################################

import os
import numpy as np
import pandas as pd
import re
import models

# # schemas done
# class Manufacturer:
#     def __init__(self, name):
#         self.name = name
#         self.id = None
# class Supplier:
#     def __init__(self, name):
#         self.name = name
#         self.id = None
# class Category:
#     def __init__(self, name):
#         self.name = name
#         self.id = None
# class Requisition:
#     def __init__(self, status):
#         self.status = status
#         self.id = None
# class Receiving:
#     def __init__(self, status):
#         self.status = status
#         self.id = None
# class PurchaseOrder:
#     def __init__(self, number):
#         self.number = number
#         self.id = None
# class Department:
#     def __init__(self, name):
#         self.name = name
#         self.id = None

# # schema done
# class User:
#     def __init__(self):
#         self.id = None
#         self.name = None

# # schema done
# class Checkout:
#     def __init__(self):
#         self.id = None
#         self.asset = None
#         self.user = None
#         self.date_out = None
#         self.date_in = None

# # schema done
# class Asset:
#     def __init__(self):
#         self.id = None
#         self.asset_id = None # DONE
#         self.description = None # DONE
#         self.is_current = None # DONE
#         self.model_number = None # DONE
#         self.serial_number = None # DONE
#         self.date_placed = None # DONE
#         self.date_removed = None # DONE
#         self.date_record_created = None
#         self.date_warranty_expires = None # DONE
#         self.cost = None # what Harvest paid # DONE
#         self.shipping = None # DONE
#         self.cost_brand_new = None # DONE
#         self.life_expectancy_years = None
#         self.notes = None # combine "status" column with this one # DONE
#         self.maint_dir = None # bool whether entered in Maintenance Direct # DONE
#         self.bulk_count = None # often 1 but several entries are bulk # DONE
        
#         self.po_number = None # purchase order number                                                        # TODO: turn into FK
#         self.requisition = None # either null, awaiting invoice, partial payment, paid in full, or donated   # TODO: turn into FK
#         self.receiving = None # either null, shipped, received, or placed                                    # TODO: turn into FK
#         self.asset_class1 = None # type                                                                      # TODO: turn into FK
#         self.asset_class2 = None # specific type                                                             # TODO: turn into FK
#         self.manufacturer = None                                                                             # TODO: turn into FK
#         self.supplier = None                                                                                 # TODO: turn into FK
#         self.department = None                                                                               # TODO: turn into FK
        
#         self.area = None
    
#     def __str__(self):
#         s = "Asset ID: " + "'"+str(self.asset_id)+"'\n"
#         s += "Asset Description: " + "'"+str(self.description)+"'\n"
#         s += "Asset Bulk Count: " + str(self.bulk_count)
#         return s
    

# class Account:
#     def __init__(self):
#         self.id = None
#         self.number = None
#         self.description = None
    
#     def __str__(self):
#         s = "~~~Account~~~\n"
#         s += "Account number: " + self.number + "\n"
#         s += "Account description: " + (self.description if self.description is not None else "<unassigned>")
#         s += "\n\n"
#         return s

# # schema done
# class Far:
#     def __init__(self):
#         self.id = None
#         self.account = None
#         self.description = None # have a "TODO" account to mark assets that might be added to the FAR in the future
#         self.pdf = None
#         self.start_date = None # when depreciation starts
#         self.life = None # in years
    
#     def __str__(self):
#         s = "~~~Far~~~\n"
#         s += ">>>>>Far account\n" + str(self.account) + "\n"
#         s += ">>>>>Far pdf: " + self.pdf
#         s += "\n\n"
#         return s

# # schema done
# class AssetFar: # m2m
#     def __init__(self, asset, far):
#         self.asset = asset
#         self.far = far
#         self.id = None
    
#     def __str__(self):
#         s = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
#         s += "~~~AssetFar association~~~\n"
#         s += "\n>>>>>Asset\n" + str(self.asset) + "\n"
#         s += "\n>>>>>Far\n" + str(self.far) + "\n"
#         return s
    
# # schema done
# class Location:
#     def __init__(self):
#         self.id = None
#         self.description = None
#         self.parent = None # reference to other location same table
#         self.children = {}
    
# # schema done
# class LocationCount:
#     def __init__(self):
#         self.id = None
#         self.asset = None
#         self.location = None# can be a default location if location is unknown (eg: add missing counts to default location during audit)
#         self.count = None # how many of that asset at location
#         self.audit_date = None # date last audited
    
# # schema done
# class Invoice:
#     def __init__(self):
#         self.id = None
#         self.number = None
#         self.filepath = None
    
#     def __str__(self):
#         return "\nInvoice path: " + self.filepath
    
# # schema done
# class AssetInvoice: # m2m assets-invoices
#     def __init__(self):
#         self.id = None
#         self.asset = None
#         self.invoice = None
    
#     def __str__(self):
#         return "\n~~~AssetInvoice: " + str(self.asset) + str(self.invoice)

# # schema done
# class Picture:
#     def __init__(self):
#         self.id = None
#         self.filepath = None
    
#     def __str__(self):
#         return "\n~~~Picture: " + self.filepath + "\n"

# # schema done
# class AssetPicture:
#     def __init__(self):
#         self.id = None
#         self.asset = None
#         self.filepath = None
    
#     def __str__(self):
#         return "\n~~~AssetPicture: " + str(self.asset) + str(self.filepath)


    
def get_df(file, sheet):
    #xl = pd.ExcelFile(file)
    #df = xl.parse(sheet)
    df = pd.read_excel(file, sheet_name=sheet, dtype=str)
    return df


df = get_df('input/asset_list.xlsx', 'merge')

# #########################################################
# print the last 20 items in column 'Classification'
#current = list(df.loc[:,'Classification'])
#last_few = current[-20:]
#for x in last_few:
#    print(str(x))
#print(str(type(current[-20])))

#print(list(df.columns.values))
#print(df.loc[:,'asset_id'])
#print(list(df.columns.values))
#print(df.loc[:,'asset_id'])


# #############################################################
# TODO: take most fields from assets.xlsx as is to craft part of the insert statement:
asset_id = "item_number_db"
description = "Description"
#   Classification --> is_current (1 if "Current", 0 if "Previous", null if ""
is_current = "Classification"
model_number = "Model Number"
serial_number = "Serial Number"
date_placed = "Placed in Service"
date_removed = "Removed From Service"
date_warranty_expires ="Warranty Expiration Date"
cost = "Original Cost (Total) / (Est.) what Harvest paid"
life_expectancy_years = "Life Expectancy"
#   "Status" --> append to notes
notes = "Notes"
cost_brand_new = "Brand New Replacement Cost / List Price"
shipping = "SHIPPING COST"
asset_class1 = "Type"
asset_class2 = "Specific Type"
bulk_count = "Bulk Entry Count"
maint_dir = "Online System (MaintDir or AssetTiger)"


# ##############################################################
# Populate choices
manufacturers = {key:models.Manufacturer(key) for key in list(df.loc[:,"Manufacturer"])}
suppliers = {key:models.Supplier(key) for key in list(df.loc[:,"Supplier"])}
categories = {key:models.Category(key) for key in list(df.loc[:,"Type"])}
categories.update({key:models.Category(key) for key in list(df.loc[:,"Specific Type"])})
departments = {key:models.Department(key) for key in list(df.loc[:,"Department"])}
requisitions = {key:models.Requisition(key) for key in list(df.loc[:,"REQUISITION"])}
receiving = {key:models.Receiving(key) for key in list(df.loc[:,"RECEIVING"])}

PO_REGEX = re.compile("PO-[0-9]{6}")
def get_POs():
    PO_list = []
    for val in list(df.loc[:,"Notes"]):
        po = re.search(PO_REGEX, val)
        if po:
            PO_list.append(po.group(0))
    return PO_list
purchase_orders = {key:models.PurchaseOrder(key) for key in get_POs()}


# ##############################################################
# Create assets dictionary - most data read into memory here ?
def convert_to_dbcurrency(s):
    """takes a str representing money value with optional decimal part"""
    precision = 10
    if s == "nan":
        return None
    parts = None
    if "." in s:
        parts = s.split(".")
        assert(len(parts)==2)
        parts[1] = parts[1].ljust(precision, '0')
    else:
        parts = [s,"".ljust(precision, '0')] # left and right of decimal point
    return "".join(parts)


def populate_asset_from_row(asset, row):
    """args: row -> df row, asset -> Asset"""
    key = row[asset_id]
    asset.asset_id = row[asset_id]
    asset.description = row[description]
    
    is_curr = row[is_current]
    asset.is_current = (lambda c : 1 if str(is_curr)=="Current" else (0 if str(is_curr)=="Previous" else None))(is_curr)
    
    asset.model_number = row[model_number]
    asset.serial_number = row[serial_number]

    asset.date_placed = row[date_placed]
    asset.date_removed = row[date_removed]
    asset.date_warranty_expires = row[date_warranty_expires]
    
    asset.cost = convert_to_dbcurrency(row[cost])
    asset.shipping = convert_to_dbcurrency(row[shipping])
    asset.cost = convert_to_dbcurrency(row[cost_brand_new])
    
    years = row[life_expectancy_years]
    asset.life_expectancy_years = (lambda y : int(years) if years != "nan" else None)(years)

    mnotes = row[notes]
    status = row['Status']
    if (status != "" and status != "nan"):
        mnotes = mnotes + "  Status: " + status
    asset.notes = mnotes
    
    mmaint_dir = row[maint_dir].lower()
    asset.maint_dir = (lambda there : 1 if mmaint_dir == "maintdir" else 0)(mmaint_dir)
    
    # bulk entries
    bulk_count = row["Bulk Entry Count"]
    try:
        asset.bulk_count = int(bulk_count)
    except:
        pass
    
    # set PO #s
    po = re.search(PO_REGEX, row[notes])
    if po:
        asset.po_number = po.group(0)

    asset.requisition = row["REQUISITION"]
    asset.receiving = row["RECEIVING"]
    asset.asset_class1 = row["Type"]
    asset.asset_class2 = row["Specific Type"]
    asset.manufacturer = row["Manufacturer"]
    asset.supplier = row["Supplier"]
    asset.department = row["Department"]
    
    return str(key), asset

assets = {}
for index, row in df.iterrows():
    asset = models.Asset()
    key, asset = populate_asset_from_row(asset, row)
    if key in assets:
        print(str(key) + " already exists.")
        raise Exception
    assets[key] = asset

#from pprint import pprint
#pprint(vars(assets['mus-67']))


# ##############################################################################
# TODO: take FAR, asset pics, and invoice pics and "OTHER LINKS" from new_cleaning.xlsx
df2 = get_df('input/new_cleaning.xlsx', 'new_cleaning')


not_in_cleaning = 0
todo_account = models.Account()
todo_account.number = "TODO"
todo_account.description = "Any items linked to this account may need to be added to FAR."
todo_far = models.Far()
todo_far.account = todo_account
todo_far.pdf = "<none>"
fars = {"TODO":todo_far} # key is acct:pdf (format: ######:#[#[#]]) # TODO
accounts = {"TODO":todo_account} # TODO
asset_fars = [] # TODO
pictures = {}
asset_pics = []
invoices = {}
asset_invoices = []
root_location = models.Location()
root_location.description = "Earth"

FAR_REGEX = re.compile("[0-9]{5}:([0-9]{1,}|na)")
import ast
import locations_import
for index, row in df2.iterrows():
    try:
        assert(row['Item Number'] in assets)
    except:
        print("Asset id in new_cleaning.xlsx needing import because it was not found in asset_list.xlsx: " + row['Item Number'])
        not_in_cleaning = not_in_cleaning + 1
        continue
    asset = assets[row['Item Number']]
    
    # ###############################
    # FAR
    far = row['FAR']
    
    if far != 'nan':
        fs = far.split(";")
        for f in fs:
            # validate
            try:
                assert(re.match(FAR_REGEX,f) or f=="TODO" or f=="nan")
            except:
                print("far format assertion failed: " + f)
                exit()
            # add to fars, accounts, asset_fars
            if f=="nan":
                continue
            elif f=="TODO":
                #asset = assets[row['Item Number']]
                far = fars['TODO']
                af = models.AssetFar(asset, far)
                asset_fars.append(af)
            else:
                #asset = assets[row['Item Number']]
                # f has format ######:#[#[#]] (acct:pdf)
                parts = f.split(":")
                acct = parts[0]
                pdf = parts[1]
                if f in fars:
                    af = models.AssetFar(asset, fars[f])
                    asset_fars.append(af)
                else:
                    if acct in accounts:
                        a = accounts[acct]
                    else:
                        a = models.Account()
                        a.number = acct
                        accounts[acct] = a
                    far = models.Far()
                    far.account = a
                    far.pdf = pdf
                    fars[f] = far
                    af = models.AssetFar(asset, far)
                    asset_fars.append(af)
                    
                        
    
    # ###############################
    # Asset Pics
    pics = row['Pics']
    pics_list = ast.literal_eval(pics)
    for pic in pics_list:
        if pic not in pictures:
            p = models.Picture()
            p.filepath = pic
            pictures[pic] = p
        ap = models.AssetPicture()
        ap.asset = asset
        ap.filepath = p
        asset_pics.append(ap)
    
    # ###############################
    # Invoices
    invoice_paths = row['Invoice pics']
    invoice_list = ast.literal_eval(invoice_paths)
    for invoice in invoice_list:
        if invoice not in invoices:
            i = models.Invoice()
            i.filepath = invoice
            invoices[invoice] = i
        ai = models.AssetInvoice()
        ai.asset = asset
        ai.invoice = i
        asset_invoices.append(ai)


df3 = get_df('input/new_cleaning_locations.xlsx', 'new_cleaning')
for index, row in df3.iterrows():
    # ###############################
    # Locations
    # TODO: print out that module's location_counts
    locs_str = row['db_location']
    asset = assets[row['Item Number']]
    root_location = locations_import.parse_locations(asset, locs_str, root_location)

    
print(len(assets)) # 5770...but only 5767 assets will be give locations?  TODO: query db once imported to see which ones are missing location counts

# TODO: import into sqlite db via pandas dataframe


# ##################################################################################################
# TEST asset results
#for k,v in assets.items():
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
for loc_count in locations_import.location_counts:
    if loc_count.asset.bulk_count is not None:
        print("\n#################################")
        print(str(loc_count))
