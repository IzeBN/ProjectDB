-- laba 9

-- exercize 1

select
	concat(
		substring(fname FROM 1 FOR 1),
		substring(mname FROM 1 FOR 1),
		'_', birthday, '_',
		lname
	) as data
from stud
where birthday between '1983-01-01' and '1992-12-31';

-- exercize 2

select
	upper(stud.lname) as lastname,
	stud.birthday
from stud
join gruppa on gruppa.gruppa_id = stud.fk_gruppa_id
where gruppa.gruppa in ('302', '375', '386');

-- exercize 3

select
	stud.nozach,
	stud.lname
from stud
join gruppa on gruppa.gruppa_id = stud.fk_gruppa_id
where gruppa.gruppa in ('303', '305')
order by stud.lname;

-- exercize 4

select *
from prepod
order by lname, fname, mname;

-- exercize 5

select 
	count(*) as stud_count,
	min(birthday) as min_birthday,
	max(birthday) as max_birthday
from stud;

-- exercize 6

select
	gruppa.gruppa,
	count(stud.*)
from gruppa
join stud on stud.fk_gruppa_id = gruppa.gruppa_id
group by gruppa.gruppa;

-- exercize 7

select
	gruppa.gruppa,
	count(stud.*)
from gruppa
join stud on stud.fk_gruppa_id = gruppa.gruppa_id
group by gruppa.gruppa
HAVING COUNT(stud.*) < 20;
