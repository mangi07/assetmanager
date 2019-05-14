/*
File: test.sql

Create: 4/29/2019

Description: test queries on db created with import.sql
  Not fully test.
*/


-- set up requisition lookup table
insert into requisition (status) values ('awaiting invoice'),('partial payment'),('paid in full'),('donated');

-- more fields can be added later, some default
insert into asset (asset_id, description) values ('test1', 'test1 desc');

select * from asset;

-- need to create a category to be associated with asset
insert into category (name) values ('category1');

-- associate asset with category
update asset set category_1=1 where id=1;

-- select asset and include its category_1 association
select asset.asset_id, asset.description, category.name from asset inner join category on asset.category_1 = category.id;

-- insert 2nd category name to category table so the following asset query will show asset1
insert into category (name) values ('category2');

-- update asset1 to include category2
update asset set category_2=1 where id=1;

-- select asset and associated category names
select asset.asset_id, asset.description, cat1.name as cat1, cat2.name as cat2 from asset
  left join category cat1 on asset.category_1 = cat1.id
  left join category cat2 on asset.category_2 = cat2.id;

-- select location counts for a particular asset
select asset.asset_id, asset.description, location.description, location_count.count from asset
  inner join location_count on asset.id = location_count.asset
  inner join location on location_count.location = location.id
where asset.asset_id = 'folding-chairs-mity-lite-swiftset';

-- select invoice file paths associated with asset ids
select asset.asset_id, invoice.file_path from asset
inner join asset_invoice on asset_invoice.asset = asset.id
inner join invoice on asset_invoice.invoice = invoice.id;

-- select list of asset-far associations
select asset.asset_id, far.description, account.number, far.pdf from asset
inner join asset_far on asset.id = asset_far.asset
inner join far on asset_far.far = far.id
inner join account on far.account = account.id;

-- select list of asset-invoice associations
select asset.asset_id, asset.description, invoice.number, invoice.file_path from asset
inner join asset_invoice on asset_invoice.asset = asset.id
inner join invoice on asset_invoice.invoice = invoice.id;

-- select number of assets that have invoice associations
select count(distinct asset.asset_id) from asset
inner join asset_invoice on asset_invoice.asset = asset.id;

-- -----------------------
-- reset tables --
-- -----------------------
delete from asset;
delete from account;
delete from asset_far;
delete from asset_invoice;
delete from asset_picture;
delete from checkout;
delete from category;
delete from department;
delete from far;
delete from invoice;
delete from location;
delete from location_count;
delete from manufacturer;
delete from picture;
delete from purchase_order;
delete from receiving;
delete from requisition;
delete from sqlite_sequence;
delete from supplier;
delete from user;

-- set up requisition lookup table
insert into requisition (status) values ('awaiting invoice'),('partial payment'),('paid in full'),('donated');

insert into receiving (status) values ('shipped'), ('received'), ('placed');