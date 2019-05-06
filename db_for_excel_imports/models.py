# schemas done
class Manufacturer:
    def __init__(self, name):
        self.name = name
        self.id = None
class Supplier:
    def __init__(self, name):
        self.name = name
        self.id = None
class Category:
    def __init__(self, name):
        self.name = name
        self.id = None
class Requisition:
    def __init__(self, status):
        self.status = status
        self.id = None
class Receiving:
    def __init__(self, status):
        self.status = status
        self.id = None
class PurchaseOrder:
    def __init__(self, number):
        self.number = number
        self.id = None
class Department:
    def __init__(self, name):
        self.name = name
        self.id = None

# schema done
class User:
    def __init__(self):
        self.id = None
        self.name = None

# schema done
class Checkout:
    def __init__(self):
        self.id = None
        self.asset = None
        self.user = None
        self.date_out = None
        self.date_in = None

# schema done
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
    
# schema done
class Invoice:
    def __init__(self):
        self.id = None
        self.number = None
        self.filepath = None
    
    def __str__(self):
        return "\nInvoice path: " + self.filepath
    
# schema done
class AssetInvoice: # m2m assets-invoices
    def __init__(self):
        self.id = None
        self.asset = None
        self.invoice = None
    
    def __str__(self):
        return "\n~~~AssetInvoice: " + str(self.asset) + str(self.invoice)

# schema done
class Picture:
    def __init__(self):
        self.id = None
        self.filepath = None
    
    def __str__(self):
        return "\n~~~Picture: " + self.filepath + "\n"

# schema done
class AssetPicture:
    def __init__(self):
        self.id = None
        self.asset = None
        self.filepath = None
    
    def __str__(self):
        return "\n~~~AssetPicture: " + str(self.asset) + str(self.filepath)
