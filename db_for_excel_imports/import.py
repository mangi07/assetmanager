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
# ###################################################################

import os
import numpy as np
import pandas as pd

# schemas done
class Manufacturer:
    id = None
    name = None
class Supplier:
    id = None
    name = None
class Category:
    id = None
    name = None
class Requisition:
    id = None
    status = None
class Receiving:
    id = None
    status = None
class PurchaseOrder:
    id = None
    number = None
class Department:
    id = None
    name = None

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
    requisition = None # either null, awaiting invoice, partial payment, paid in full, or donated
    receiving = None # either null, shipped, received, or placed
    asset_class1 = None # type
    asset_class2 = None # specific type
    model_number = None # DONE
    serial_number = None # DONE
    area = None
    bulk_count = None # often 1 but several entries are bulk
    date_placed = None # DONE
    date_removed = None # DONE
    date_record_created = None
    date_warranty_expires = None # DONE
    manufacturer = None
    supplier = None
    cost = None # what Harvest paid # DONE
    shipping = None # DONE
    po_number = None # purchase order number
    cost_brand_new = None # DONE
    life_expectancy_years = None
    notes = None # combine "status" column with this one
    department = None
    maint_dir = None # bool whether entered in Maintenance Direct

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
#blanks = [s for s in current if s != "Current" and s != "Previous"]
#blanks = [s for s in current if type(s)==float]


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

    
    return str(key), asset

assets = {}
for index, row in df.iterrows():
    asset = Asset()
    key, asset = populate_asset_from_row(asset, row)
    if key in assets:
        raise Exception
    assets[key] = asset

#
#
# TODO: take FAR, asset pics, and invoice pics from new_cleaning.xlsx
#
# TODO: take some other fields (belonging to other tables) and create their objects if they don't exist and add FK to asset object:
#   example: if asset has "Manufacturer" Goodman, try to find it in list of Manufacture objects.
#       If it doesn't exist, create the object with name Goodman, set id, and assign this id to manufacturer field of asset object.
#   The mappings are:
#       "Manufacturer" --> manufacturer,
#       "Supplier" --> supplier,
#       "INVOICE/ORDER/RECEIPT #" and "INVOICE LINK"--> AssetInvoice and Invoice and use first pic with invoice #
#           but if more than 1 invoice pic, link asset to "TODO" invoice,
#       "Department" --> department
#
#
# TODO: scan through ./input/asset_list.xlsx and ./input/new_cleaning.xlsx and see if there are any assets yet to be added
# TODO: import into sqlite db via pandas dataframe


