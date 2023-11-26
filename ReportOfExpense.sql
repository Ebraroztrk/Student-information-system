use ReportOfExpense;
create table Employee(
	employee_id int,
	salary int,
	primary key(employee_id)
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
	in_stock boolean,
	primary key (material_id)
);
create table Additional_Expenses(
	expense_id int,
	week_no ENUM(1,2,3,4),
	material_id int,
	name varchar(20),
	amount int,
	primary key (expense_id),
	foreign key (material_id) references Material(material_id)
);
create table Course_Uses_Material(
	course_id int,
	material_id int,
	week_no ENUM(1,2,3,4);
	primary key (course_id,material_id),
	foreign key (material_id) references Material(material_id)
	foreign key (course_id) references Course(course_id)
);
create table Course(
	course_id int,
	material_id int,
	primary key (course_id),
	foreign key (material_id) references Material(material_id)
);

