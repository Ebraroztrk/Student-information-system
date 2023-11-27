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
create table Course(
	course_id int,
	primary key (course_id)
);
create table Course_Uses_Material(
	course_id int,
	material_id int,
	week_no int,
	primary key (course_id,material_id),
	foreign key (material_id) references Material(material_id),
	foreign key (course_id) references Course(course_id)
);




-- bir material kalmadiysa ve harhangi bir hafta onu kullanmak isteyen course olursa uyari gonderir.
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


