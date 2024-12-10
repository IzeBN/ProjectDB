---- ВАРИАНТ №27

-- exercize 1
select 
	concat(fname, ' ', mname) as name_fatherly,
	concat(lname, ' ', fk_gruppa_id) as lastname_group,
	concat(lname, ' ', fname, ' ', mname) as fio
from stud;

-- exercize 2
select
	concat(
		to_char(birthday, 'DD'),
		lower(substring(fname FROM 1 FOR 3)),
		to_char(birthday, 'MM'),
		lower(substring(mname FROM 1 FOR 3)),
		to_char(birthday, 'YY'),
		lower(substring(lname FROM 1 FOR 3))
	) as uuid,
	concat(lname, ' ', fname) as name_lastname,
	nozach
from stud;

-- exercize 3
select 
	distinct birthday
from stud;

-- exercize 4
select 
	concat(lname, ' ', fname, ' ', mname, ' - ', birthday) as fio_birthdat
from prepod
where length(lname) = 7;

-- exercize 5
select
	concat(stud.lname, ' ',
		upper(substring(stud.fname FROM 1 FOR 1)), '.',
		upper(substring(stud.mname FROM 1 FOR 1)), '.'
	) as inicials,
	stud.birthday,
	extract (year from age('2009-09-01', stud.birthday)) as age
from stud
	left join pol on stud.fk_pol_id = pol.pol_id
where pol.pol_short = 'М'
	and extract (year from age('2009-09-01', stud.birthday)) > extract (day from stud.birthday);

-- exercize 6 НЕТУ ПОЛА ПРЕПОДОВАТЕЛЕЙ В ТАБЛИЦЕ, СДЕЛАЛ ДЛЯ СТУДЕНТОВ
select
	concat(stud.lname, ' ',
		upper(substring(stud.fname FROM 1 FOR 1)), '.',
		upper(substring(stud.mname FROM 1 FOR 1)), '.'
	) as inicials,
	stud.birthday,
	concat(to_char(stud.birthday, 'MM'), ' - ',
		case
			when extract (month from stud.birthday) in (12, 1, 2) then 'Зима'
			when extract (month from stud.birthday) in (3, 4, 5) then 'Весна'
			when extract (month from stud.birthday) in (6, 7, 8) then 'Лето'
			when extract (month from stud.birthday) in (9, 10, 11) then 'Осень'
		end
	)
from stud
	left join pol on pol.pol_id = stud.fk_pol_id
where pol.pol_short = 'М';