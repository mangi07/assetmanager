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
# ###################################################################

import os
import numpy as np
import pandas as pd
import re

# schemas done
class Manufacturer:
    def __init__(self, name):
        self.name = name
    id = None
class Supplier:
    def __init__(self, name):
        self.name = name
    id = None
class Category:
    def __init__(self, name):
        self.name = name
    id = None
class Requisition:
    def __init__(self, status):
        self.status = status
    id = None
class Receiving:
    def __init__(self, status):
        self.status = status
    id = None
class PurchaseOrder:
    def __init__(self, number):
        self.number = number
    id = None
class Department:
    def __init__(self, name):
        self.name = name
    id = None

# schema done
class User:
    id = None
    name = None

# schema done
class Checkout:
    id = None
    asset = None
    user = None
    date_out = None
    date_in = None

# schema done
class Asset:
    id = None
    asset_id = None # DONE
    description = None # DONE
    is_current = None # DONE
    model_number = None # DONE
    serial_number = None # DONE
    date_placed = None # DONE
    date_removed = None # DONE
    date_record_created = None
    date_warranty_expires = None # DONE
    cost = None # what Harvest paid # DONE
    shipping = None # DONE
    cost_brand_new = None # DONE
    life_expectancy_years = None
    notes = None # combine "status" column with this one # DONE
    maint_dir = None # bool whether entered in Maintenance Direct # DONE
    bulk_count = None # often 1 but several entries are bulk # DONE
    
    po_number = None # purchase order number                                                        # TODO: turn into FK
    requisition = None # either null, awaiting invoice, partial payment, paid in full, or donated   # TODO: turn into FK
    receiving = None # either null, shipped, received, or placed                                    # TODO: turn into FK
    asset_class1 = None # type                                                                      # TODO: turn into FK
    asset_class2 = None # specific type                                                             # TODO: turn into FK
    manufacturer = None                                                                             # TODO: turn into FK
    supplier = None                                                                                 # TODO: turn into FK
    department = None                                                                               # TODO: turn into FK
    
    area = None
    

class Account:
    id = None
    number = None
    description = None

# schema done
class Far:
    id = None
    account = None
    description = None # have a "TODO" account to mark assets that might be added to the FAR in the future
    pdf = None
    start_date = None # when depreciation starts
    life = None # in years

# schema done
class AssetFar: # m2m
    id = None
    asset = None
    far = None # if marked by default entry
    
# schema done
class Location:
    id = None
    description = None
    parent = None # reference to other location same table
    
# schema done
class LocationCount:
    id = None
    asset = None
    location = None# can be a default location if location is unknown (eg: add missing counts to default location during audit)
    count = None # how many of that asset at location
    audit_date = None # date last audited
    
# schema done
class Invoice:
    id = None
    number = None
    filepath = None
    
# schema done
class AssetInvoice: # m2m assets-invoices
    id = None
    asset = None
    invoice = None

# schema done
class Picture:
    id = None
    filepath = None

# schema done
class AssetPicture:
    id = None
    asset = None
    filepath = None


    
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
manufacturers = {key:Manufacturer(key) for key in list(df.loc[:,"Manufacturer"])}
suppliers = {key:Supplier(key) for key in list(df.loc[:,"Supplier"])}
categories = {key:Category(key) for key in list(df.loc[:,"Type"])}
categories.update({key:Category(key) for key in list(df.loc[:,"Specific Type"])})
departments = {key:Department(key) for key in list(df.loc[:,"Department"])}
requisitions = {key:Requisition(key) for key in list(df.loc[:,"REQUISITION"])}
receiving = {key:Receiving(key) for key in list(df.loc[:,"RECEIVING"])}

PO_REGEX = re.compile("PO-[0-9]{6}")
def get_POs():
    PO_list = []
    for val in list(df.loc[:,"Notes"]):
        po = re.search(PO_REGEX, val)
        if po:
            PO_list.append(po.group(0))
    return PO_list
purchase_orders = {key:PurchaseOrder(key) for key in get_POs()}


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
    asset = Asset()
    key, asset = populate_asset_from_row(asset, row)
    if key in assets:
        raise Exception
    assets[key] = asset

#from pprint import pprint
#pprint(vars(assets['mus-67']))


# ##############################################################################
# TODO: take FAR, asset pics, and invoice pics and "OTHER LINKS" from new_cleaning.xlsx
df2 = get_df('input/new_cleaning.xlsx', 'new_cleaning')

# ######################
# FAR
# class Account:
#     id = None
#     number = None
#     description = None

# # schema done
# class Far:
#     id = None
#     account = None
#     description = None # have a "TODO" account to mark assets that might be added to the FAR in the future
#     pdf = None
#     start_date = None # when depreciation starts
#     life = None # in years

# # schema done
# class AssetFar: # m2m
#     id = None
#     asset = None
#     far = None # if marked by default entry
    

not_in_cleaning = 0
fars = {} # TODO
accounts = {} # TODO
asset_fars = {} # TODO

for index, row in df2.iterrows():
    try:
        assert(row['Item Number'] in assets)
    except:
        print("Asset id in new_cleaning.xlsx needing import because it was not found in asset_list.xlsx: " + row['Item Number'])
        not_in_cleaning = not_in_cleaning + 1
        
    # FAR
    far = row['FAR']
    FAR_REGEX = re.compile("[0-9]{5}:([0-9]{1,}|na)")
    if far != 'nan':
        fars = far.split(";")
        for f in fars:
            # validate
            try:
                assert(re.match(FAR_REGEX,f) or f=="TODO" or f=="nan")
            except:
                print("far format assertion failed: " + f)
                exit()
            # add to farss, accounts, asset_fars
    #print(far)
print("Number of assets not in asset_list.xlsx: " + str(not_in_cleaning))

# # schema done
# class Location:
#     id = None
#     description = None
#     parent = None # reference to other location same table
#
# # schema done
# class LocationCount:
#     id = None
#     asset = None
#     location = None# can be a default location if location is unknown (eg: add missing counts to default location during audit)
#     count = None # how many of that asset at location
#     audit_date = None # date last audited
    
# # schema done
# class Invoice:
#     id = None
#     number = None
#     filepath = None
    
# # schema done
# class AssetInvoice: # m2m assets-invoices
#     id = None
#     asset = None
#     invoice = None

# # schema done
# class Picture:
#     id = None
#     filepath = None

# # schema done
# class AssetPicture:
#     id = None
#     asset = None
#     filepath = None



# TODO: scan through ./input/asset_list.xlsx and ./input/new_cleaning.xlsx and see if there are any assets yet to be added
# TODO: import into sqlite db via pandas dataframe


