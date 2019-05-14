# done
class Manufacturer:
    def __init__(self, name):
        self.name = name
        self.id = None
    def list_vals(self):
        return [self.id, self.name]
    def list_column_names():
        return ["id", "name"]
        
# done
class Supplier:
    def __init__(self, name):
        self.name = name
        self.id = None
    def list_vals(self):
        return [self.id, self.name]
    def list_column_names():
        return ["id", "name"]
        
# done
class Category:
    def __init__(self, name):
        self.name = name
        self.id = None
    def list_vals(self):
        return [self.id, self.name]
    def list_column_names():
        return ["id", "name"]
        
# done
class Requisition:
    def __init__(self, status):
        self.status = status
        self.id = None
    def list_vals(self):
        return [self.id, self.status]
    def list_column_names():
        return ["id", "status"]
        
# done
class Receiving:
    def __init__(self, status):
        self.status = status
        self.id = None
    def list_vals(self):
        return [self.id, self.status]
    def list_column_names():
        return ["id", "status"]
        
# done
class PurchaseOrder:
    def __init__(self, number):
        self.number = number
        self.id = None
    def list_vals(self):
        return [self.id, self.number]
    def list_column_names():
        return ["id", "number"]
        
# done
class Department:
    def __init__(self, name):
        self.name = name
        self.id = None
    def list_vals(self):
        return [self.id, self.name]
    def list_column_names():
        return ["id", "name"]


class User:
    def __init__(self):
        self.id = None
        self.name = None


class Checkout:
    def __init__(self):
        self.id = None
        self.asset = None
        self.user = None
        self.date_out = None
        self.date_in = None


class Asset:
    def __init__(self):
        self.id = None
        self.asset_id = None # DONE
        self.description = None # DONE
        self.is_current = None # DONE
        self.model_number = None # DONE
        self.serial_number = None # DONE
        self.date_placed = None # DONE
        self.date_removed = None # DONE
        self.date_record_created = None
        self.date_warranty_expires = None # DONE
        self.cost = None # what Harvest paid # DONE
        self.shipping = None # DONE
        self.cost_brand_new = None # DONE
        self.life_expectancy_years = None
        self.notes = None # combine "status" column with this one # DONE
        self.maint_dir = None # bool whether entered in Maintenance Direct # DONE
        self.bulk_count = None # often 1 but several entries are bulk # DONE
        
        self.po_number = None # purchase order number                                                        # TODO: turn into FK
        self.requisition = None # either null, awaiting invoice, partial payment, paid in full, or donated   # TODO: turn into FK
        self.receiving = None # either null, shipped, received, or placed                                    # TODO: turn into FK
        self.asset_class1 = None # type                                                                      # TODO: turn into FK
        self.asset_class2 = None # specific type                                                             # TODO: turn into FK
        self.manufacturer = None                                                                             # TODO: turn into FK
        self.supplier = None                                                                                 # TODO: turn into FK
        self.department = None                                                                               # TODO: turn into FK
        
        self.area = None
    
    def __str__(self):
        s = "Asset ID: " + "'"+str(self.asset_id)+"'\n"
        s += "Asset Description: " + "'"+str(self.description)+"'\n"
        s += "Asset Bulk Count: " + str(self.bulk_count) + "\n"
        return s
    
    def list_vals(self):
        return [self.id,
                self.asset_id,
                self.description,
                self.is_current,
                self.requisition,
                self.receiving,
                self.asset_class1,
                self.asset_class2,
                self.model_number,
                self.serial_number,
                self.bulk_count if self.bulk_count is not None else 1,
                self.date_placed,
                self.date_removed,
                self.date_warranty_expires,
                self.manufacturer,
                self.supplier,
                self.cost,
                self.shipping,
                self.po_number,
                self.cost_brand_new,
                self.life_expectancy_years,
                self.notes,
                self.department,
                self.maint_dir]

    
    def list_column_names():
        return ["id",
                "asset_id",
                "description",
                "is_current",
                "requisition",
                "receiving",
                "category_1",
                "category_2",
                "model_number",
                "serial_number",
                "bulk_count",
                "date_placed",
                "date_removed",
                "date_warranty_expires",
                "manufacturer",
                "supplier",
                "cost",
                "shipping",
                "purchase_order",
                "cost_brand_new",
                "life_expectancy_years",
                "notes",
                "department",
                "maint_dir"]
    

class Account:
    def __init__(self):
        self.id = None
        self.number = None
        self.description = None
    
    def __str__(self):
        s = "~~~Account~~~\n"
        s += "Account number: " + self.number + "\n"
        s += "Account description: " + (self.description if self.description is not None else "<unassigned>")
        s += "\n\n"
        return s
        
    def list_vals(self):
        return [self.id, self.number, self.description]
    def list_column_names():
        return ["id", "number", "description"]


# schema done
class Far:
    def __init__(self):
        self.id = None
        self.account = None
        self.description = None # have a "TODO" account to mark assets that might be added to the FAR in the future
        self.pdf = None
        self.start_date = None # when depreciation starts
        self.life = None # in years
    
    def __str__(self):
        s = "~~~Far~~~\n"
        s += ">>>>>Far account\n" + str(self.account) + "\n"
        s += ">>>>>Far pdf: " + self.pdf
        s += "\n\n"
        return s
    
    def list_vals(self):
        return [self.id, self.account, self.description, self.pdf, self.life]
    def list_column_names():
        return ["id", "account", "description", "pdf", "life"]

# schema done
class AssetFar: # m2m
    def __init__(self, asset, far):
        self.asset = asset
        self.far = far
        self.id = None
    
    def __str__(self):
        s = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        s += "~~~AssetFar association~~~\n"
        s += "\n>>>>>Asset\n" + str(self.asset) + "\n"
        s += "\n>>>>>Far\n" + str(self.far) + "\n"
        return s
    
    def list_vals(self):
        return [self.asset, self.far]
    def list_column_names():
        return ["asset", "far"]


# schema done
class Location:
    def __init__(self):
        self.id = None
        self.description = None
        self.parent = None # reference to other location same table
        self.children = {}
    
    def __str__(self):
        if self.parent is None:
            return self.description
        return str(self.parent) + " >> " + str(self.description) # recursion expands this string

    def list_vals(self):
        return [self.id, self.description, self.parent.id if self.parent is not None else None]
    def list_column_names():
        return ["id", "description", "parent"]


# schema done
class LocationCount:
    def __init__(self):
        self.id = None
        self.asset = None
        self.location = None# can be a default location if location is unknown (eg: add missing counts to default location during audit)
        self.count = None # how many of that asset at location
        self.audit_date = None # date last audited
        
    def __str__(self):
        return "\n~~~LocationCount: " + str(self.asset) + str(self.location) + "\nCount: " + str(self.count)
    
    def list_vals(self):
        return [self.id, self.asset, self.location, self.count, self.audit_date]
    def list_column_names():
        return ["id", "asset", "location", "count", "audit_date"]


# schema done
class Invoice:
    def __init__(self):
        self.id = None
        self.number = None
        self.filepath = None
    
    def __str__(self):
        return "\nInvoice path: " + self.filepath
        
    def list_vals(self):
        return [self.id, self.number, self.filepath]
    def list_column_names():
        return ["id", "number", "file_path"]
    
# schema done
class AssetInvoice: # m2m assets-invoices
    def __init__(self):
        self.id = None
        self.asset = None
        self.invoice = None
    
    def __str__(self):
        return "\n~~~AssetInvoice: " + str(self.asset) + str(self.invoice)
    
    def list_vals(self):
        return [self.asset, self.invoice]
    def list_column_names():
        return ["asset", "invoice"]

# schema done
class Picture:
    def __init__(self):
        self.id = None
        self.filepath = None
    
    def __str__(self):
        return "\n~~~Picture: " + self.filepath + "\n"
    
    def list_vals(self):
        return [self.id, self.filepath]
    def list_column_names():
        return ["id", "file_path"]
   

# schema done
class AssetPicture:
    def __init__(self):
        self.id = None
        self.asset = None
        self.filepath = None
    
    def __str__(self):
        return "\n~~~AssetPicture: " + str(self.asset) + str(self.filepath)
    
    def list_vals(self):
        return [self.asset, self.filepath]
    def list_column_names():
        return ["asset", "picture"]

