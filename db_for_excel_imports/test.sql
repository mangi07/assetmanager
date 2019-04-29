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

-- select asset and include multiple related fields
select asset.asset_id, asset.description, cat1.name, cat2.name from asset
  inner join category cat1 on asset.category_1 = cat1.id
  inner join category cat2 on asset.category_2 = cat2.id;
  
