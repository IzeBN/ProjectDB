-- exercize 1
select * from stud;

-- exercize 2
select 
	lname,
	rost
from stud;

-- exercize 3
select
	lname,
	rost
from stud
where ves >= 50 and ves <= 75;

-- exercize 4

select
	stud.*
from stud
left join gruppa on gruppa.gruppa_id = stud.fk_gruppa_id
where gruppa.gruppa = '384';

-- exercize 5
select
	stud.*
from stud
left join pol on pol.pol_id = stud.fk_pol_id
where pol.pol_short = 'М';

-- exercize 6
select
	stud.*
from stud
left join pol on pol.pol_id = stud.fk_pol_id
left join gruppa on gruppa.gruppa_id = stud.fk_gruppa_id
where pol.pol_short = 'Ж' and gruppa.gruppa != '384';

-- exercie 7
select *
from stud
where fname like 'а%' or lname like '%ов';

-- exercize 8
select
	upper(lname) as lastname,
	upper(fname) as name
from stud
where mname like 'Ал%';

-- exercize 9

select
	upper(substring(stud.lname FROM 1 FOR 5)) as lastname,
	lower(substring(stud.fname FROM 1 FOR 2)) as name
from stud
left join gruppa on gruppa.gruppa_id = stud.fk_gruppa_id
where gruppa.gruppa = '384';
