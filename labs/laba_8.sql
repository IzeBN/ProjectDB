-- exercize 1
select 
	lname,
	fname,
	birthday
from stud
where extract(month from birthday) = 1
and extract(dow from birthday) = 1;

-- exercize 2
select
	lname,
	birthday
from stud
where (extract(month from birthday) in (5, 9, 8))
and (lname like 'А%' or lname like '%ж%');

-- exercize 3
select
	concat(lname, ' ', fname, ' ', mname),
	concat('№ ', nozach),
	birthday
from stud
where extract(month from birthday) in (9, 10, 11)
and extract(year from age(now(), birthday)) < 40;

-- exercize 4
select *
from stud
where birthday between '1989-7-10' and '1989-7-31';