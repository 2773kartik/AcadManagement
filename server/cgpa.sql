DELIMITER //
CREATE PROCEDURE calculate_sgpa_and_update_student(IN input_session_id INT)
BEGIN
    DECLARE stu_id INT;
    DECLARE cgpa FLOAT;

    -- Calculate SGPA and update stu_sg for each student
    INSERT INTO stu_sg (s_id, ses_id, sg, creds)
    SELECT
        stu_course.stu_id,
        input_session_id AS ses_id,
        SUM(stu_course.grade * course.c_cred) / SUM(course.c_cred) AS sg,
        SUM(course.c_cred) AS creds
    FROM stu_course
    INNER JOIN course ON stu_course.course_id = course.c_id
    WHERE stu_course.course_session = input_session_id
    GROUP BY stu_course.stu_id;

    -- Calculate CGPA and update student table for each student
    UPDATE student s
    SET
        cgpa = (
            SELECT SUM(grade * c_cred) / SUM(c_cred) AS overall_cgpa
            FROM stu_course
            INNER JOIN course ON stu_course.course_id = course.c_id
            WHERE stu_course.stu_id = s.s_id AND stu_course.status = 4
            AND stu_course.course_session = input_session_id
        ),
        credits = (
            SELECT SUM(c_cred) AS total_credits
            FROM stu_course
            INNER JOIN course ON stu_course.course_id = course.c_id
            WHERE stu_course.stu_id = s.s_id AND stu_course.status = 4
            AND stu_course.course_session = input_session_id
        )
    WHERE s.s_id IN (SELECT DISTINCT stu_id FROM stu_course WHERE course_session = input_session_id);
END //
DELIMITER ;
