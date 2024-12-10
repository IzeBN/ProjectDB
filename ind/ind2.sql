---- ВАРИАНТ 27

-- exercize 1
select 
	concat('Группа №', fk_gruppa_id),
	count(*) as count_tud,
	avg(rost) as sred_rost
from stud
	group by fk_gruppa_id;

-- самая рослая группа:
select 
	concat('Группа №', fk_gruppa_id),
	count(*) as count_tud,
	avg(rost) as most
from stud
	group by fk_gruppa_id
	order by most desc
	limit 1;

-- exercize 2
select 
	to_char(birthday, 'MM') as birthmonth,
	count(*) as count_students,
	avg(rost) as sred_rost,
	min(ves) as minimal_weight
from stud
where rost > 1.70
	group by birthmonth;

-- самый легкий студент:
select 
	to_char(birthday, 'MM') as month,
	ves
from stud
	order by ves asc
	limit 1;

-- exercize 3
select 
    pol.pol_short as ps,
    floor(ves / 10) * 10 as weight_group,
    count(*) as count_stud
from stud
	left join pol on pol.pol_id = stud.fk_pol_id
	group by ps, weight_group
	order by ps, weight_group;

