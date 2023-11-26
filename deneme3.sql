use deneme3;

CREATE TABLE Teacher (
    teacher_id INT not null,
    course_id int unique,
    PRIMARY KEY (teacher_id)
);
CREATE TABLE Student (
    student_id INT,
    PRIMARY KEY (student_id)
);
CREATE TABLE Course (
	course_id int,
    teacher_id INT,
    day_section INT CHECK(day_section >= 0 AND day_section <= 69),
    request_count int default 0,
    active BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (course_id,day_section),
    FOREIGN KEY (teacher_id) REFERENCES Teacher(teacher_id)
);

create table student_request(
	student_id int,
	course_id int,
	primary key(student_id,course_id),
	foreign key (course_id) references Course(course_id),
    foreign key (student_id) references Student(student_id)
);

CREATE TABLE Section_Request (
	request_id int auto_increment,
    day_section INT CHECK(day_section >= 00 AND day_section <= 69),
    course_id int,
    PRIMARY KEY (request_id),
    foreign key (course_id) references Course(course_id)
);

CREATE TABLE Teacher_Section_Availability(
    teacher_id INT,
    course_id int,
    available_section INT,
    PRIMARY KEY (teacher_id, available_section),
    FOREIGN KEY (teacher_id) REFERENCES Teacher(teacher_id)
);
CREATE TABLE Student_Section_Availability (
    student_id INT,
    available_section INT,
    PRIMARY KEY (student_id, available_section),
    FOREIGN KEY (student_id) REFERENCES Student(student_id)
);

create table teacher_program(
	teacher_id int,
	day_section int CHECK(day_section >= 00 AND day_section <= 69),
	course_id int,
	PRIMARY KEY (day_section, teacher_id),
	foreign key (course_id) references Course(course_id),
    FOREIGN KEY (teacher_id) REFERENCES Teacher(teacher_id)
);
create table student_program(
	student_id int,
	day_section int CHECK(day_section >= 00 AND day_section <= 69),
	course_id int,
	PRIMARY KEY (day_section, student_id),
	foreign key (course_id) references Course(course_id),
    foreign key (student_id) references Student(student_id)
);

CREATE TRIGGER after_insert_teacher_avail
AFTER INSERT ON Teacher_Section_Availability
FOR EACH ROW
BEGIN
    INSERT INTO course
    VALUES (new.course_id, NEW.teacher_id, new.available_section,0,false);
END;


CREATE TRIGGER section_request_trigger
AFTER INSERT ON Section_Request
FOR EACH ROW
begin
    UPDATE course
    SET request_count = request_count + 1
    WHERE day_section = new.day_section and course_id = new.course_id;
END;

-- insertions--
-- -------------------------------------------------
-- 10 numarali ogretmeni ekledik(100 numarali kursu veriyor)
insert into teacher 
values(10,100);
-- 10 numarali ogretmen pzt, sali full bos
-- triggerdan dolayi ders tablosu icin ogretmenin musait oldugu saatler icin non-active sekilde dersler ekleniyor
insert into Teacher_Section_Availability
values(10,100,00),(10,100,01),(10,100,02),(10,100,03),(10,100,04),
	  (10,100,10),(10,100,11),(10,100,12),(10,100,13),(10,100,14);
-- rastgele ogrenciler 100 kodlu der acilsin diye farkli saatler icin istekte bulunuyor	 
-- 2 kisi carsamba 1. section olsun demis, 2 kisi sali gunu 1. section olsun demis, 1 kisi sali gunu 0. section olsun demis
-- max requesti alan ve ogretmenin musait oldugu saat olan sali gunu 1. sectiona ders konulmali
-- insertler bitince course 100 icin 11 degeri active hale gelecek 
insert into section_request
values(1,21,100),(2,21,100),(3,11,100),(4,11,100),(5,10,100);
-- --------------------------------------------------
insert into teacher 
values(11,101);
insert into Teacher_Section_Availability
values(11,101,20),(11,101,21),(11,101,22),(11,101,23),(11,101,24),(11,101,25);
insert into section_request
values(6,21,101),(7,22,101),(8,30,101),(9,30,101),(10,30,101);
-- ---------------------------------------------------
insert into teacher 
values(12,102);
insert into Teacher_Section_Availability
values(12,102,30),(12,102,31),(12,102,32);
insert into section_request
values(11,22,102),(12,32,102),(13,30,102),(14,30,102);


select *
from course c ;

-- max sayida talep edilen zamana dersi aktive ediyor.
-- max 2 tane ise 2 tane ders aciliyor.
UPDATE course
SET active = true 
WHERE course_id IN (
    SELECT course_id
    FROM (
        SELECT course_id, MAX(request_count) AS max_request_count
        FROM course
        GROUP BY course_id
    ) AS max_counts
    WHERE request_count = max_request_count
);

-- debug course
select *
from course c ;

-- bir ogretmenin verdigi ders hangi saatlerde aktif olmus
INSERT INTO teacher_program (teacher_id, day_section, course_id)
select c.teacher_id,c.day_section,c.course_id
FROM Course c
where c.active = true;

-- teacher debug
select *
from teacher_program tp;

-- ----------------------------------------
insert into student 
values(1);
insert into student_section_availability 
values(1,22);
insert into student_request 
values(1,102),(1,101);


INSERT INTO student_program (student_id, day_section, course_id)
select sr.student_id,c.day_section,c.course_id
from student_request sr
JOIN Course c ON sr.course_id = c.course_id
where c.active = TRUE;

select *
from student_program sp;

select *
from course c ;



















	 
	 
	 