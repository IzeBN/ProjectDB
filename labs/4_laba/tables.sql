CREATE TABLE IF NOT EXISTS job_title(
		job_id VARCHAR(128) PRIMARY KEY,
		title VARCHAR(64),
		salary INT
	);

CREATE TABLE IF NOT EXISTS employee(
		employee_id varchar(128) PRIMARY KEY,
		date_birth TIMESTAMP,
		adress VARCHAR(256),
		phone_number BIGINT,
		cabinet VARCHAR(16),
		job_title VARCHAR(128),
		FOREIGN KEY (job_title) REFERENCES job_title(job_id)
	);

CREATE TABLE IF NOT EXISTS project(
		project_id VARCHAR(128) PRIMARY KEY,
		project_title VARCHAR(512),
		executor_id VARCHAR(128),
		supervisor_id VARCHAR(128),
		FOREIGN KEY (executor_id) REFERENCES employee(employee_id),
		FOREIGN KEY (supervisor_id) REFERENCES employee(employee_id)
	);
