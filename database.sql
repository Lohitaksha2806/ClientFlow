CREATE DATABASE video_editing_db;
USE video_editing_db;
CREATE TABLE Clients (
    client_id INT PRIMARY KEY AUTO_INCREMENT,
    client_name VARCHAR(100) NOT NULL,
    phone VARCHAR(15),
    email VARCHAR(100),
    company_name VARCHAR(100),
    joined_date DATE
);
CREATE TABLE Projects (
    project_id INT PRIMARY KEY AUTO_INCREMENT,
    client_id INT,
    project_name VARCHAR(100) NOT NULL,
    project_type VARCHAR(50),
    start_date DATE,
    deadline DATE,
    status VARCHAR(20) CHECK (status IN ('Pending', 'In Progress', 'Completed')),
    budget DECIMAL(10,2),
    FOREIGN KEY (client_id) REFERENCES Clients(client_id)
);
CREATE TABLE Editors (
    editor_id INT PRIMARY KEY AUTO_INCREMENT,
    editor_name VARCHAR(100),
    specialization VARCHAR(100),
    experience_years INT
);
CREATE TABLE Project_Assignment (
    assignment_id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT,
    editor_id INT,
    assigned_date DATE,
    FOREIGN KEY (project_id) REFERENCES Projects(project_id),
    FOREIGN KEY (editor_id) REFERENCES Editors(editor_id)
);
CREATE TABLE Revisions (
    revision_id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT,
    revision_number INT,
    revision_notes TEXT,
    revision_date DATE,
    FOREIGN KEY (project_id) REFERENCES Projects(project_id)
);
CREATE TABLE Payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT,
    amount_paid DECIMAL(10,2),
    payment_date DATE,
    payment_method VARCHAR(50),
    payment_status VARCHAR(20) CHECK (payment_status IN ('Paid', 'Pending', 'Partial')),
    FOREIGN KEY (project_id) REFERENCES Projects(project_id)
);

CREATE VIEW PendingPaymentsView AS
SELECT
    p.project_name,
    c.client_name,
    pay.amount_paid,
    pay.payment_status
FROM Projects p
JOIN Clients c ON p.client_id = c.client_id
JOIN Payments pay ON p.project_id = pay.project_id
WHERE pay.payment_status != 'Paid';

DELIMITER //

CREATE PROCEDURE AddPayment(
    IN p_project_id INT,
    IN p_amount DECIMAL(10,2),
    IN p_method VARCHAR(50),
    IN p_status VARCHAR(20)
)
BEGIN
    INSERT INTO Payments(project_id, amount_paid, payment_date, payment_method, payment_status)
    VALUES (p_project_id, p_amount, CURDATE(), p_method, p_status);
END //

DELIMITER ;

DELIMITER //

CREATE TRIGGER update_project_status
AFTER INSERT ON Payments
FOR EACH ROW
BEGIN
    DECLARE total_paid DECIMAL(10,2);
    DECLARE project_budget DECIMAL(10,2);

    SELECT SUM(amount_paid)
    INTO total_paid
    FROM Payments
    WHERE project_id = NEW.project_id;

    SELECT budget
    INTO project_budget
    FROM Projects
    WHERE project_id = NEW.project_id;

    IF total_paid >= project_budget THEN
        UPDATE Projects
        SET status = 'Completed'
        WHERE project_id = NEW.project_id;
    END IF;
END //

DELIMITER ;

