CREATE PROCEDURE IF NOT EXISTS after_current_update(IN user_id INTEGER, IN user_level INTEGER, IN user_ip VARCHAR(255))
            BEGIN
                UPDATE current_session 
                SET active=FALSE 
                WHERE ip = user_ip AND (id != user_id OR level != user_level);
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

                -- Get user details
                SELECT id, level INTO user_id, user_level
                FROM current_session
                WHERE ip = input_ip AND active = TRUE;

                -- Check if the user has level 2
                IF user_id IS NOT NULL AND user_level = 2 THEN
                    -- Check if the course_id has user_id as p_id
                    SELECT p_id INTO prof_id
                    FROM course
                    WHERE c_id = input_course_id
                    LIMIT 1;

                    -- Check if prof_id is not null and matches user_id
                    IF prof_id IS NOT NULL AND prof_id = user_id THEN
                        -- Get the active session ID
                        SELECT s_id INTO session_id
                        FROM session
                        WHERE active = TRUE
                        LIMIT 1;

                        -- Insert into stu_course
                        INSERT INTO stu_course(course_id, course_session, stu_id, status, grade)
                        SELECT input_course_id, session_id, s_id, 3, 0
                        FROM student
                        WHERE s_year = input_year AND s_degree = input_degree AND s_dept = input_dept
                        LIMIT 1;

                        SELECT 'success' AS status;
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

                -- Get user details
                SELECT id, (SELECT s_id FROM session WHERE active = TRUE) INTO user_id, active_session
                FROM current_session
                WHERE ip = input_ip AND active = TRUE AND level = 2;

                -- Check if the user has level 2 and an active session is set
                IF user_id IS NOT NULL AND active_session IS NOT NULL THEN
                    -- Proceed with the course insert
                    INSERT INTO course(c_name, c_cred, c_session, p_id)
                    VALUES (input_name, input_cred, active_session, user_id);

                    IF ROW_COUNT() = 1 THEN
                        SELECT 'success' AS status;
                    ELSE
                        SELECT 'failed' AS status;
                    END IF;
                ELSE
                    SELECT 'permission denied' AS status;
                END IF;
            END;