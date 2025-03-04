# When considering total number of items purchased from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?
# The data provided dose not contain rewars receipt status as "Accepted", so considering "Finished".
select REWARDSRECEIPTSTATUS, sum(purchaseditemcount) as total_count from receipts
where REWARDSRECEIPTSTATUS in('FINISHED','REJECTED') group by REWARDSRECEIPTSTATUS;