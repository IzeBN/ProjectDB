---- ВАРИАНТ 27

-- exercize 1 
select
	concat(sp.codocso, '.', sp.specialnost) as specialnost,
	kaf.kafedra,
	concat(gruppa.gruppa, ' гр.') as gruppa,
	sub.shortsubject
from gruppa
	left join specialnost as sp on sp.specialnost_id = gruppa.fk_specialnost_id
	left join faculty as fac on fac.faculty_id = gruppa.fk_faculty_id
	left join kurs as kur on kur.kurs_id = gruppa.fk_kurs_id
	left join semestr as sem on sem.fk_kurs_id = kur.kurs_id
	left join ekzamen as ek on ek.fk_semestr_id = sem.semestr_id
	left join subject as sub on sub.subject_id = ek.fk_subject_id
	left join prepod as pr on pr.prepod_id = ek.fk_prepod_id
	left join kafedra as kaf on kaf.kafedra_id = pr.fk_kafedra_id
where fac.facshort = 'ИФМО'
	group by
		sp.codocso,
		sp.specialnost,
		kaf.kafedra,
		gruppa.gruppa,
		sub.shortsubject,
		fac.facshort;

-- exercize 2
select 
	concat(sp.specialnost, ' (', sp.codocso, ')') specialnost,
	concat(kurs.kurs_id, ' курс') kurs,
	sub.shortsubject,
	tp.coment
from ackbook
	left join stud on stud.stud_id = ackbook.fk_stud_id
	left join gruppa on gruppa.gruppa_id = stud.fk_gruppa_id
	left join ekzamen as ekz on ekz.ekzamen_id = ackbook.fk_ekzamen_id
	left join subject as sub on sub.subject_id = ekz.fk_subject_id
	left join specialnost as sp on sp.specialnost_id = gruppa.fk_specialnost_id
	left join kurs on kurs.kurs_id = gruppa.fk_kurs_id
	left join typeoch as tp on tp.typeoch_id = ackbook.fk_typeoch_id
where tp.typeoch in (0, 2, 10, 11);

-- exercize 3

select 
	concat(stud.lname, ' ',
		upper(substring(stud.fname FROM 1 FOR 1)), '.',
		upper(substring(stud.mname FROM 1 FOR 1)), '.'
	) as inicials,
	count(ac.*) as count_ekzams,
	avg(tp.typeoch) as sred_bal,
	count(case when tp.typeoch = 5 then 1 end) as count_fives
from stud
	left join gruppa on gruppa.gruppa_id = stud.fk_gruppa_id
	left join ackbook as ac on ac.fk_stud_id = stud.stud_id
	left join typeoch as tp on tp.typeoch_id = ac.fk_typeoch_id
where gruppa.gruppa = '3011'
	group by inicials
