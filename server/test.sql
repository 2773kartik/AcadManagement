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
INSERT INTO student(s_name, s_email, s_roll, s_password, s_degree, s_year, s_dept) VALUES('Kartik Tiwari', '2021csb1102@iitrpr.ac.in', '2021CSB1102', 'password', 'B.Tech', 2, 1);
/
INSERT INTO student(s_name, s_email, s_roll, s_password, s_degree, s_year, s_dept) VALUES('Harshit Gupta', '2021csb1092@iitrpr.ac.in', '2021CSB1092', 'password', 'B.Tech', 2, 1);
/
INSERT INTO student(s_name, s_email, s_roll, s_password, s_degree, s_year, s_dept) VALUES('Akshit Singh', '2021mcb1228@iitrpr.ac.in', '2021mcb1228', 'password', 'B.Tech', 2, 2);
