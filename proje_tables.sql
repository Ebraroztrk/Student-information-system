use ubs;
create table Person(
	person_id int,
	age int,
	mail varchar(20),
	tel_no char(11),
	address varchar(50),
	name varchar(15),
	surname varchar(15),
	primary key(person_id)
);

create table Student(
    student_id int,
    department varchar(20),
    primary key(student_id),
    foreign key (student_id) references Person(person_id)
);

create table Graduated_student(
 	student_id int,
 	graduate_date date,
 	grade double check(grade>=0 and grade<=4),
	primary key (student_id),
	foreign key (student_id) references Student(student_id)
)

create table Active_student(
 	student_id int,
	primary key (student_id),
	foreign key (student_id) references Student(student_id)
);

create table Parents(
	student_id int,
	mail varchar(20),
	tel_no char(11),
	name_surname varchar(30),
	primary key(student_id),
	foreign key (student_id) references Student(student_id)
);

create table Employee(
	employee_id int,
	salary int,
	primary key (employee_id)
	foreign key (employee_id) references Person(person_id)
);

create table Administrative_staff(
	personel_id int,
	foreign key (personel_id) references Employee(employee_id)
);
create table Temizlikci(
	temizlikci_id int,
	foreign key (temizlikci_id) references Employee(employee_id)
);
create table Report(
	report_id int,
	monthly_weekly boolean,
	primary key(report_id)
);
create table Expenses(
	expense_id int,
	report_id int,
	primary key (expense_id),
	foreign key (report_id) references Report(report_id)	
);
create table Fixed_Expense(
	expense_id int,
	total_salary int,
	rent int,
	cleaning_expense int,
	primary key (expense_id),
	foreign key (expense_id) references Expenses(expense_id)
);
create table Material(
	material_id int,
	amount int,
	stock_amount int,
	primary key (material_id)
);
create table Additional_Expenses(
	expense_id int,
	week_no int,
	material_id int,
	name varchar(20),
	amount int,
	primary key (expense_id),
	foreign key (material_id) references Material(material_id)
);
CREATE TABLE Teacher (
    teacher_id INT not null,
    course_id int unique,
    PRIMARY KEY (teacher_id),
    foreign key (teacher_id) references Employee(employee_id)
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
create table Course_Uses_Material(
	course_id int,
	material_id int,
	week_no int,
	primary key (course_id,material_id),
	foreign key (material_id) references Material(material_id),
	foreign key (course_id) references Course(course_id)
);

create table student_request(
	student_id int,
	course_id int,
	primary key(student_id,course_id),
	foreign key (course_id) references Course(course_id),
    foreign key (student_id) references Active_student(student_id)
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
    FOREIGN KEY (student_id) REFERENCES Active_student(student_id)
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
    foreign key (student_id) references Active_student(student_id)
);

-- -----------------------------------------------


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


CREATE PROCEDURE RaiseMaterialStockEmptyWarning()
BEGIN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Warning: Material stock is empty for material_id ';
END;

CREATE TRIGGER CourseUsesMaterialTrigger
AFTER INSERT ON Course_Uses_Material
FOR EACH ROW
BEGIN
    -- Update the material amount by decrementing it by 1
    UPDATE Material
    SET amount = amount - 1
    WHERE material_id = NEW.material_id;

    -- Set stock_available using SELECT INTO
    SET @stock_available = (
        SELECT amount
        FROM Material
        WHERE material_id = NEW.material_id
    );

    -- If the stock is empty, call the stored procedure to raise a warning
    IF @stock_available <= 0 THEN
        CALL RaiseMaterialStockEmptyWarning();
    END IF;
END;


CREATE TRIGGER after_insert_on_Student_program
AFTER INSERT ON student_program
FOR EACH ROW
BEGIN
    DELETE FROM student_section_availability ssa
    WHERE ssa.available_section = NEW.day_section AND ssa.student_id = NEW.student_id;
END;
-- -------------------------------------------------------------------------
