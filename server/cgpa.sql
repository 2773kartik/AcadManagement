CREATE PROCEDURE calculate_sgpa(IN input_session_id INT)
BEGIN
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
END;

/
CREATE PROCEDURE update_cgpa()
BEGIN
    UPDATE student
    SET cgpa = (
        SELECT SUM(sg * creds) / SUM(creds) AS overall_cgpa
        FROM stu_sg
        WHERE s_id = student.s_id
    ),
    credits = (
        SELECT SUM(creds) AS total_credits
        FROM stu_sg
        WHERE s_id = student.s_id
    );
END;