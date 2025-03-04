# When considering average spend from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?
# The data provided dose not contain rewars receipt status as "Accepted", so considering "Finished".
select REWARDSRECEIPTSTATUS, avg(totalspent) as avg_spend from receipts
where REWARDSRECEIPTSTATUS in('FINISHED','REJECTED') group by REWARDSRECEIPTSTATUS