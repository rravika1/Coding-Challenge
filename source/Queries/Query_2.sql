# How does the ranking of the top 5 brands by receipts scanned for the recent month compare to the ranking for the previous month?

select b.name as brand_name, count(ri.receiptitemid) as receipts_scanned, 'recent month' as month,row_number() over (order by count(ri.receiptitemid) desc) as brand_rank
from receiptitems ri
join receipts r on ri.receiptid = r.receiptid
join brands b on ri.barcode = b.barcode
where date_format(r.datescanned, '%Y-%m') = date_format((select max(datescanned) from receipts), '%Y-%m')
group by b.name

union all

select b.name as brand_name, count(ri.receiptitemid) as receipts_scanned,'previous month' as month,row_number() over (order by count(ri.receiptitemid) desc) as brand_rank
from receiptitems ri
join receipts r on ri.receiptid = r.receiptid
join brands b on ri.barcode = b.barcode
where date_format(r.datescanned, '%Y-%m') = date_format((select max(datescanned) from receipts) - interval 1 month, '%Y-%m')
group by b.name
order by month, brand_rank;