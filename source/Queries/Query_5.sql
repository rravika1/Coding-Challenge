# Which brand has the most spend among users who were created within the past 6 months?

select b.name as brand_name, sum(ri.itemprice * ri.QuantityPurchased) as total_spend
from users u
join receipts r on u.userid = r.userid
join receiptitems ri on r.receiptid = ri.receiptid
join brands b on ri.barcode = b.barcode
where u.createddate >= (select date_sub(max(createddate), interval 6 month) from users)
group by b.name
order by total_spend desc
limit 1;