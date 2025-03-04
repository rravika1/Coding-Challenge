# What are the top 5 brands by receipts scanned for most recent month?

select b.Name as brand_name, count(ri.ReceiptItemID) as receipts_scanned from receiptitems ri 
join receipts r on ri.ReceiptID = r.ReceiptID 
join brands b on ri.Barcode = b.Barcode
where date_format(r.DateScanned,'%Y-%m') = date_format((select max(DateScanned) from receipts),'%Y-%m')
group by b.Name 
order by receipts_scanned desc limit 5;