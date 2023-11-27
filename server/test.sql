INSERT INTO admin(username, password) VALUES('admin', 'admin');
/
INSERT INTO dept(d_name) VALUES('CSE');
/
INSERT INTO dept(d_name) VALUES('MNC');
/
INSERT INTO dept(d_name) VALUES('ELE');
/
INSERT INTO proff(p_name, p_email, p_password, d_id) VALUES('Apurva Mudgal', 'apurva@iitrpr.ac.in', 'password', 1);
/
INSERT INTO proff(p_name, p_email, p_password, d_id) VALUES('Sandeep Kumar', 'sandeep@iitrpr.ac.in', 'password', 2);
/
INSERT INTO proff(p_name, p_email, p_password, d_id) VALUES('Jagpreet Singh', 'jagpreet@iitrpr.ac.in', 'password', 1);
/
INSERT INTO proff(p_name, p_email, p_password, d_id) VALUES('Sudarshan Iyengar', 'sudarshan@iitrpr.ac.in', 'password', 1);
/
INSERT INTO proff(p_name, p_email, p_password, d_id) VALUES('Pradeep Duhan', 'pradeep@iitrpr.ac.in', 'password', 3);
/
INSERT INTO proff(p_name, p_email, p_password, d_id) VALUES('Anil Kumar', 'anil@iitrpr.ac.in', 'password', 2);
/
INSERT INTO session(s_name, active) VALUES('2023-S1', TRUE);
/
INSERT INTO session(s_name, active) VALUES('2023-S2', FALSE);
/
-- Students with degree B.Tech or M.Tech, dept 1, 2, or 3, and year 2020 or 2021
INSERT INTO student(s_name, s_email, s_roll, s_password, s_degree, s_year, s_dept) VALUES('Kartik Tiwari', '2021csb1102@iitrpr.ac.in', '2021CSB1102', 'password', 'B.Tech', 2021, 1);
/
INSERT INTO student(s_name, s_email, s_roll, s_password, s_degree, s_year, s_dept) VALUES('Harshit Gupta', '2021csb1092@iitrpr.ac.in', '2021CSB1092', 'password', 'B.Tech', 2021, 1);
/
INSERT INTO student(s_name, s_email, s_roll, s_password, s_degree, s_year, s_dept) VALUES('Akshit Singh', '2021mcb1228@iitrpr.ac.in', '2021MCB1228', 'password', 'B.Tech', 2021, 2);
/
INSERT INTO student(s_name, s_email, s_roll, s_password, s_degree, s_year, s_dept) VALUES('Rahul Sharma', '2021mcb1201@iitrpr.ac.in', '2021MCB1201', 'password', 'B.Tech', 2021, 2);
/
INSERT INTO student(s_name, s_email, s_roll, s_password, s_degree, s_year, s_dept) VALUES('Aditi Gupta', '2020cse5021@iitrpr.ac.in', '2020MCB5021', 'password', 'B.Tech', 2020, 3);
/
INSERT INTO student(s_name, s_email, s_roll, s_password, s_degree, s_year, s_dept) VALUES('Rohan Verma', '2020cse5025@iitrpr.ac.in', '2020CSB5025', 'password', 'B.Tech', 2020, 3);
/
INSERT INTO student(s_name, s_email, s_roll, s_password, s_degree, s_year, s_dept) VALUES('Neha Singh', '2020eee3050@iitrpr.ac.in', '2020EEB3050', 'password', 'B.Tech', 2020, 1);
/
INSERT INTO student(s_name, s_email, s_roll, s_password, s_degree, s_year, s_dept) VALUES('Ankit Kumar', '2020eee3078@iitrpr.ac.in', '2020EEB3078', 'password', 'B.Tech', 2020, 1);
/
INSERT INTO student(s_name, s_email, s_roll, s_password, s_degree, s_year, s_dept) VALUES('Nisha Verma', '2020mec2045@iitrpr.ac.in', '2020MCB2045', 'password', 'M.Tech', 2020, 2);
/
INSERT INTO student(s_name, s_email, s_roll, s_password, s_degree, s_year, s_dept) VALUES('Alok Yadav', '2020mec2032@iitrpr.ac.in', '2020MCB2032', 'password', 'M.Tech', 2020, 2);
/
INSERT INTO course(c_name, c_cred, c_session, p_id) VALUES('CS101', 3, 1, 1);
/
INSERT INTO course(c_name, c_cred, c_session, p_id) VALUES('CS301', 4, 2, 4);
/
INSERT INTO course(c_name, c_cred, c_session, p_id) VALUES('CS201', 4, 1, 2);
/
INSERT INTO course(c_name, c_cred, c_session, p_id) VALUES('CS401', 3, 1, 3);