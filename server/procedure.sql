CREATE PROCEDURE IF NOT EXISTS after_current_update(IN user_id INTEGER, IN user_level INTEGER, IN user_ip VARCHAR(255))
            BEGIN
                UPDATE current_session 
                SET active=FALSE 
                WHERE ip = user_ip AND (id != user_id OR level != user_level);
            END;
/
CREATE PROCEDURE session_add(
    IN input_ip VARCHAR(255),
    IN input_name VARCHAR(255)
)
BEGIN
    DECLARE user_id INT;

    -- Check if the current user has level == 3
    SELECT id INTO user_id
    FROM current_session
    WHERE ip = input_ip AND active = TRUE AND level = 3;

    IF user_id IS NOT NULL THEN
        -- The user has level == 3, proceed with the session insert
        IF NOT EXISTS (SELECT 1 FROM session WHERE s_name = input_name) THEN
            INSERT INTO session(s_name, active)
            VALUES(input_name, FALSE);

            SELECT 'success' AS status;
        ELSE
            SELECT 'Already exists!' AS status;
        END IF;
    ELSE
        SELECT 'permission denied' AS status;
    END IF;
END;
/
CREATE PROCEDURE student_add(
    IN input_name VARCHAR(255),
    IN input_password VARCHAR(255),
    IN input_year VARCHAR(255),
    IN input_roll VARCHAR(255),
    IN input_dept VARCHAR(255),
    IN input_email VARCHAR(255),
    IN input_degree VARCHAR(255),
    IN input_ip VARCHAR(255)
)
BEGIN
    DECLARE user_level INT;

    -- Check if the current user has level == 3
    SELECT level INTO user_level
    FROM current_session
    WHERE ip = input_ip AND active = TRUE AND level = 3;

    IF user_level IS NOT NULL THEN
        -- The user has level == 3, proceed with the student insert
        IF NOT EXISTS (SELECT 1 FROM student WHERE s_roll = input_roll) THEN
            INSERT INTO student(s_name, s_email, s_roll, s_password, s_degree, s_year, s_dept)
            VALUES (input_name, input_email, input_roll, input_password, input_degree, input_year, input_dept);

            SELECT 'success' AS status;
        ELSE
            SELECT 'Already exists!' AS status;
        END IF;
    ELSE
        SELECT 'permission denied' AS status;
    END IF;
END;
/

CREATE PROCEDURE student_login(
    IN input_username VARCHAR(255),
    IN input_password VARCHAR(255),
    IN input_ip VARCHAR(255)
)
BEGIN
    DECLARE user_id INT;
    
    -- Check if the provided username and password are valid
    SELECT s_id INTO user_id
    FROM student
    WHERE s_email = input_username AND s_password = input_password;

    IF user_id IS NOT NULL THEN
        -- Update current_session with the user's login information
        UPDATE current_session
        SET lastlogin = NOW(), ip = input_ip, active = TRUE
        WHERE id = user_id AND level = 1;

        -- Call after_current_update stored procedure
        CALL after_current_update(user_id, 1, input_ip);

        SELECT 'success' AS status;
    ELSE
        SELECT 'failed' AS status;
    END IF;
END;
/
CREATE PROCEDURE proff_add(
    IN input_name VARCHAR(255),
    IN input_password VARCHAR(255),
    IN input_dept VARCHAR(255),
    IN input_email VARCHAR(255),
    IN input_ip VARCHAR(255)
)
BEGIN
    DECLARE user_id INT;

    -- Check if the current user has level == 3
    SELECT id INTO user_id
    FROM current_session
    WHERE ip = input_ip AND active = TRUE AND level = 3;

    IF user_id IS NOT NULL THEN
        -- Check if the proff with the provided email already exists
        IF EXISTS (SELECT 1 FROM proff WHERE p_email = input_email) THEN
            SELECT 'Already exists!' AS status;
        ELSE
            -- Insert proff details into the proff table
            INSERT INTO proff(p_name, p_email, p_password, d_id)
            VALUES (input_name, input_email, input_password, input_dept);

            SELECT 'success' AS status;
        END IF;
    ELSE
        SELECT 'permission denied' AS status;
    END IF;
END;
/
CREATE PROCEDURE proff_login(
    IN input_username VARCHAR(255),
    IN input_password VARCHAR(255),
    IN input_ip VARCHAR(255)
)
BEGIN
    DECLARE user_id INT;

    -- Check if the provided username and password match a proff
    SELECT p_id INTO user_id
    FROM proff
    WHERE p_email = input_username AND p_password = input_password;

    IF user_id IS NOT NULL THEN
        -- Update the current session details for the proff
        UPDATE current_session
        SET lastlogin = NOW(), ip = input_ip, active = TRUE
        WHERE id = user_id AND level = 2;

        -- Call the after_current_update procedure
        CALL after_current_update(user_id, 2, input_ip);

        SELECT 'success' AS status;
    ELSE
        SELECT 'failed' AS status;
    END IF;
END;
/
CREATE PROCEDURE IF NOT EXISTS student_add_course(
        IN input_ip VARCHAR(255),
        IN input_course_id INT,
        IN input_year VARCHAR(255),
        IN input_degree VARCHAR(255),
        IN input_dept VARCHAR(255)
    )
    BEGIN
        DECLARE user_id INT;
        DECLARE user_level INT;
        DECLARE prof_id INT;
        DECLARE session_id INT;
        DECLARE old_year INT;
        DECLARE old_degree VARCHAR(255);
        DECLARE old_dept INT;
        DECLARE old_course INT;
        DECLARE old_session INT;

        -- Get user details
        SELECT id, level INTO user_id, user_level
        FROM current_session
        WHERE ip = input_ip AND active = TRUE;

        -- Check if the user has level 2
        IF user_id IS NOT NULL AND user_level = 2 THEN
            -- Check if the course_id has user_id as p_id
            SELECT p_id INTO prof_id
            FROM course
            WHERE c_id = input_course_id;

            -- Check if prof_id is not null and matches user_id
            IF prof_id IS NOT NULL AND prof_id = user_id THEN
                -- Get the active session ID
                SELECT s_id INTO session_id
                FROM session
                WHERE active = TRUE;

                -- Check if a student with the same year, degree, and department has already been added
                SELECT s_year, s_degree, s_dept, course_id, course_session INTO old_year, old_degree, old_dept, old_course, old_session
                FROM stu_course, student
                WHERE stu_course.stu_id = student.s_id
                    AND stu_course.course_session = session_id
                    AND student.s_year = input_year
                    AND student.s_degree = input_degree
                    AND student.s_dept = input_dept
                    AND course_id = input_course_id 
                    AND course_session = session_id
                LIMIT 1;

                IF old_year IS NOT NULL AND old_degree IS NOT NULL AND old_dept IS NOT NULL AND old_course IS NOT NULL AND old_session IS NOT NULL THEN
                    SELECT 'already added' AS status;
                ELSE
                    -- Insert into stu_course
                    INSERT INTO stu_course(course_id, course_session, stu_id, status, grade)
                    SELECT input_course_id, session_id, s_id, 3, 0
                    FROM student
                    WHERE s_year = input_year AND s_degree = input_degree AND s_dept = input_dept;

                    SELECT 'success' AS status;
                END IF;
            ELSE
                SELECT 'permission denied' AS status;
            END IF;
        ELSE
            SELECT 'permission denied' AS status;
        END IF;
    END;

/

CREATE PROCEDURE IF NOT EXISTS add_course(
                IN input_ip VARCHAR(255),
                IN input_name VARCHAR(255),
                IN input_cred INTEGER
            )
            BEGIN
                DECLARE user_id INT;
                DECLARE active_session INT;
                DECLARE oldname VARCHAR(255);
                DECLARE oldsession INT;

                -- Get user details
                SELECT id, (SELECT s_id FROM session WHERE active = TRUE) INTO user_id, active_session
                FROM current_session
                WHERE ip = input_ip AND active = TRUE AND level = 2;

                -- Check if the user has level 2 and an active session is set
                IF user_id IS NOT NULL AND active_session IS NOT NULL THEN
                    SELECT c_name, c_session INTO oldname, oldsession
                    FROM course
                    WHERE c_name = input_name AND c_session = active_session
                    LIMIT 1;

                    IF oldname IS NOT NULL AND oldsession IS NOT NULL THEN
                        SELECT 'already added' AS status;
                    
                    ELSE
                        -- Proceed with the course insert
                        INSERT INTO course(c_name, c_cred, c_session, p_id)
                        VALUES (input_name, input_cred, active_session, user_id);

                        IF ROW_COUNT() = 1 THEN
                            SELECT 'success' AS status;
                        ELSE
                            SELECT 'failed' AS status;
                        END IF;
                    END IF;
                ELSE
                    SELECT 'permission denied' AS status;
                END IF;
            END;

/
CREATE PROCEDURE IF NOT EXISTS add_grade(
                IN input_ip VARCHAR(255),
                IN stud_id INT,
                IN input_course_id INT,
                IN input_grade INT
            )
            BEGIN
                DECLARE user_id INT;
                DECLARE active_session INT;
                DECLARE old_course INT;
                DECLARE old_session INT;

                -- Get user details
                SELECT id, (SELECT s_id FROM session WHERE active = TRUE) INTO user_id, active_session
                FROM current_session
                WHERE ip = input_ip AND active = TRUE AND level = 2;

                -- Check if the user has level 2 and an active session is set
                IF user_id IS NOT NULL AND active_session IS NOT NULL THEN
                    -- Check if the course_id has user_id as p_id
                    SELECT c_id INTO old_course
                    FROM course
                    WHERE c_id = input_course_id;

                    -- Check if old_course is not null and matches user_id
                    IF old_course IS NOT NULL THEN
                        -- Get the active session ID
                        SELECT s_id INTO old_session
                        FROM session
                        WHERE active = TRUE;

                        -- Check if the course is active in the current session
                        IF old_session IS NOT NULL AND old_session = active_session THEN
                            -- Update the grade
                            UPDATE stu_course
                            SET grade = input_grade
                            WHERE course_id = input_course_id AND course_session = active_session AND stu_id = stud_id;

                            SELECT 'success' AS status;
                        ELSE
                            SELECT 'permission denied' AS status;
                        END IF;
                    ELSE
                        SELECT 'permission denied' AS status;
                    END IF;
                ELSE
                    SELECT 'permission denied' AS status;
                END IF;
            END;

/

CREATE PROCEDURE IF NOT EXISTS get_proffs(
                IN input_ip VARCHAR(255)
            )
            BEGIN
                DECLARE user_id INT;
                DECLARE active_session INT;

                -- Get user details
                SELECT id, (SELECT s_id FROM session WHERE active = TRUE) INTO user_id, active_session
                FROM current_session
                WHERE ip = input_ip AND active = TRUE AND level = 2;

                -- Check if the user has level 2 and an active session is set
                IF user_id IS NOT NULL AND active_session IS NOT NULL THEN
                    -- Get the list of proffs
                    SELECT p_id, p_name, p_email, d_name
                    FROM proff, dept
                    WHERE proff.d_id = dept.d_id;
                ELSE
                    SELECT 'permission denied' AS status;
                END IF;
            END;
/

CREATE PROCEDURE IF NOT EXISTS get_students(
                IN input_ip VARCHAR(255)
            )
            BEGIN
                DECLARE user_id INT;
                DECLARE active_session INT;

                -- Get user details
                SELECT id, (SELECT s_id FROM session WHERE active = TRUE) INTO user_id, active_session
                FROM current_session
                WHERE ip = input_ip AND active = TRUE AND level >= 2;

                -- Check if the user has level 2 and an active session is set
                IF user_id IS NOT NULL AND active_session IS NOT NULL THEN
                    -- Get the list of students
                    SELECT s_id, s_name, s_email, s_roll, s_degree, s_year, d_name, credits, cgpa
                    FROM student, dept
                    WHERE student.s_dept = dept.d_id;
                ELSE
                    SELECT 'permission denied' AS status;
                END IF;
            END;

/
CREATE PROCEDURE IF NOT EXISTS get_cur_courses(
                IN input_ip VARCHAR(255)
            )
            BEGIN
                DECLARE user_id INT;
                DECLARE active_session INT;

                -- Get user details
                SELECT id, (SELECT s_id FROM session WHERE active = TRUE) INTO user_id, active_session
                FROM current_session
                WHERE ip = input_ip AND active = TRUE AND level >= 1;

                -- Check if the user has level 2 and an active session is set
                IF user_id IS NOT NULL AND active_session IS NOT NULL THEN
                    -- Get the list of courses
                    SELECT c_id, c_name, c_cred, p_name, d_name
                    FROM course, proff, dept
                    WHERE course.p_id = proff.p_id AND proff.d_id = dept.d_id AND c_session = active_session;
                ELSE
                    SELECT 'permission denied' AS status;
                END IF;
            END;

/

CREATE PROCEDURE IF NOT EXISTS enroll_course(
                IN input_ip VARCHAR(255),
                IN input_course_id INT
            )
            -- student enrolls in current active course
            BEGIN
                DECLARE user_id INT;
                DECLARE active_session INT;
                DECLARE old_course INT;
                DECLARE old_session INT;

                -- Get user details
                SELECT id, (SELECT s_id FROM session WHERE active = TRUE) INTO user_id, active_session
                FROM current_session
                WHERE ip = input_ip AND active = TRUE AND level = 1;

                -- Check if the user has level 1 and an active session is set
                IF user_id IS NOT NULL AND active_session IS NOT NULL THEN
                    -- Check if the course_id exists
                    SELECT c_id INTO old_course
                    FROM course
                    WHERE c_id = input_course_id;

                    -- Check if old_course is not null
                    IF old_course IS NOT NULL THEN
                        -- Get the active session ID
                        SELECT s_id INTO old_session
                        FROM session
                        WHERE active = TRUE;

                        -- Check if the course is active in the current session
                        IF old_session IS NOT NULL AND old_session = active_session THEN
                            -- Check if the student is already enrolled in the course
                            IF NOT EXISTS (SELECT 1 FROM stu_course WHERE course_id = input_course_id AND course_session = active_session AND stu_id = user_id) THEN
                                -- Insert into stu_course
                                INSERT INTO stu_course(course_id, course_session, stu_id, status, grade)
                                VALUES (input_course_id, active_session, user_id, 1, 0);

                                SELECT 'success' AS status;
                            ELSE
                                SELECT 'already enrolled' AS status;
                            END IF;
                        ELSE
                            SELECT 'permission denied' AS status;
                        END IF;
                    ELSE
                        SELECT 'permission denied' AS status;
                    END IF;
                ELSE
                    SELECT 'permission denied' AS status;
                END IF;
            END;