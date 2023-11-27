CREATE TABLE IF NOT EXISTS admin(
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            );

CREATE TABLE IF NOT EXISTS session(
                s_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                s_name VARCHAR(255) NOT NULL,
                active BOOLEAN NOT NULL
            );

CREATE TABLE IF NOT EXISTS dept(
                d_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                d_name VARCHAR(255) NOT NULL
            );

CREATE TABLE IF NOT EXISTS proff(
                p_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                p_name VARCHAR(255) NOT NULL,
                p_email VARCHAR(255) NOT NULL,
                p_password VARCHAR(255) NOT NULL,
                d_id INTEGER NOT NULL,
                FOREIGN KEY (d_id) REFERENCES dept(d_id)
            );

CREATE TABLE IF NOT EXISTS course(
                c_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                c_name VARCHAR(255) NOT NULL,
                c_cred INTEGER NOT NULL,
                c_session INTEGER NOT NULL,
                p_id INTEGER NOT NULL,
                FOREIGN KEY (p_id) REFERENCES proff(p_id),
                FOREIGN KEY (c_session) REFERENCES session(s_id)            
            );

CREATE TABLE IF NOT EXISTS student(
                s_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                s_name VARCHAR(255) NOT NULL,
                s_email VARCHAR(255) NOT NULL,
                s_roll VARCHAR(255) NOT NULL,
                s_password VARCHAR(255) NOT NULL,
                s_degree VARCHAR(255) NOT NULL,
                s_year INTEGER NOT NULL,
                s_dept INTEGER NOT NULL,
                FOREIGN KEY (s_dept) REFERENCES dept(d_id)
            );

CREATE TABLE IF NOT EXISTS stu_course(
                course_id INTEGER NOT NULL,
                course_session INTEGER NOT NULL,
                stu_id INTEGER NOT NULL,
                status INTEGER NOT NULL,
                grade INTEGER NOT NULL,
                PRIMARY KEY (course_id, course_session, stu_id),
                FOREIGN KEY (course_id) REFERENCES course(c_id),
                FOREIGN KEY (course_session) REFERENCES session(s_id),
                FOREIGN KEY (stu_id) REFERENCES student(s_id)
            );

CREATE TABLE IF NOT EXISTS current_session(
                id INTEGER,
                lastlogin DATETIME,
                level INTEGER NOT NULL,
                ip VARCHAR(255),
                active BOOLEAN NOT NULL DEFAULT FALSE,
                PRIMARY KEY (id, level)
            );