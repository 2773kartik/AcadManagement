-- Tables to be dropped
DROP TABLE IF EXISTS stu_sg;
DROP TABLE IF EXISTS stu_course;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS proff;
DROP TABLE IF EXISTS dept;
DROP TABLE IF EXISTS session;
DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS current_session;

-- Triggers to be dropped
DROP TRIGGER IF EXISTS after_admin_insert;
DROP TRIGGER IF EXISTS after_proff_insert;
DROP TRIGGER IF EXISTS after_student_insert;
DROP TRIGGER IF EXISTS before_session_change;


-- Procedures to be dropped
DROP PROCEDURE IF EXISTS session_add;
DROP PROCEDURE IF EXISTS after_current_update;
DROP PROCEDURE IF EXISTS student_add_course;
DROP PROCEDURE IF EXISTS add_course;
DROP PROCEDURE IF EXISTS student_add;
DROP PROCEDURE IF EXISTS student_login;
DROP PROCEDURE IF EXISTS proff_add;
DROP PROCEDURE IF EXISTS proff_login;
DROP PROCEDURE IF EXISTS get_proffs;
DROP PROCEDURE IF EXISTS calculate_sgpa;
DROP PROCEDURE IF EXISTS update_cgpa;
DROP PROCEDURE IF EXISTS get_students;
DROP PROCEDURE IF EXISTS get_cur_courses;