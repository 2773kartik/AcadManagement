from flask import *
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, static_folder='build/static', template_folder='build')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+os.getenv("MYSQL_USER")+':'+os.getenv("MYSQL_PASSWORD")+'@'+os.getenv("MYSQL_HOST")+'/'+os.getenv("MYSQL_DB")
CORS(app)

mysql = SQLAlchemy(app)

def dropall():
    mysql.session.execute(text(
        '''
            DROP TABLE IF EXISTS stu_course;
        '''
    ))
    mysql.session.execute(text(
        '''
            DROP TABLE IF EXISTS student;
        '''
    ))
    mysql.session.execute(text(
        '''
            DROP TABLE IF EXISTS course;
        '''
    ))
    mysql.session.execute(text(
        '''
            DROP TABLE IF EXISTS proff;
        '''
    ))
    mysql.session.execute(text(
        '''
            DROP TABLE IF EXISTS dept;
        '''
    ))
    mysql.session.execute(text(
        '''
            DROP TABLE IF EXISTS session;
        '''
    ))
    mysql.session.execute(text(
        '''
            DROP TABLE IF EXISTS admin;
        '''
    ))
    mysql.session.execute(text(
        '''
            DROP TABLE IF EXISTS current_session;
        '''
    ))
    mysql.session.execute(text(
        '''
            DROP TRIGGER IF EXISTS after_admin_insert;
        '''
    ))
    mysql.session.execute(text(
        '''
            DROP TRIGGER IF EXISTS after_proff_insert;
        '''
    ))
    mysql.session.execute(text(
        '''
            DROP TRIGGER IF EXISTS after_student_insert;
        '''
    ))
    mysql.session.execute(text(
        '''
            DROP TRIGGER IF EXISTS after_current_update;
        '''
    ))
    mysql.session.execute(text(
        '''
            DROP PROCEDURE IF EXISTS after_current_update;
        '''
    ))
    mysql.session.execute(text(
        '''
            DROP PROCEDURE IF EXISTS student_add_course;
        '''
    ))
    mysql.session.execute(text(
        '''
            DROP PROCEDURE IF EXISTS add_course;
        '''
    ))
    mysql.session.commit()

def create_tables():
    mysql.session.execute(text(
        '''
            CREATE TABLE IF NOT EXISTS admin(
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            );
        '''
    ))
    mysql.session.execute(text(
        '''
            CREATE TABLE IF NOT EXISTS session(
                s_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                s_name VARCHAR(255) NOT NULL,
                active BOOLEAN NOT NULL
            );
        '''
    ))
    mysql.session.execute(text(
        '''
            CREATE TABLE IF NOT EXISTS dept(
                d_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                d_name VARCHAR(255) NOT NULL
            );
        '''
    ))
    mysql.session.execute(text(
        '''
            CREATE TABLE IF NOT EXISTS proff(
                p_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                p_name VARCHAR(255) NOT NULL,
                p_email VARCHAR(255) NOT NULL,
                p_password VARCHAR(255) NOT NULL,
                d_id INTEGER NOT NULL,
                FOREIGN KEY (d_id) REFERENCES dept(d_id)
            );
        '''
    ))
    mysql.session.execute(text(
        '''
            CREATE TABLE IF NOT EXISTS course(
                c_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                c_name VARCHAR(255) NOT NULL,
                c_cred INTEGER NOT NULL,
                c_session INTEGER NOT NULL,
                p_id INTEGER NOT NULL,
                FOREIGN KEY (p_id) REFERENCES proff(p_id),
                FOREIGN KEY (c_session) REFERENCES session(s_id)            
            );
        '''
    ))
    mysql.session.execute(text(
        '''
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
        '''
    ))
    mysql.session.execute(text(
        '''
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
        '''
    ))
    mysql.session.execute(text(
        '''
            CREATE TABLE IF NOT EXISTS current_session(
                id INTEGER,
                lastlogin DATETIME,
                level INTEGER NOT NULL,
                ip VARCHAR(255),
                active BOOLEAN NOT NULL DEFAULT FALSE,
                PRIMARY KEY (id, level)
            )
        '''
    ))

def add_triggers():
    mysql.session.execute(text(
        '''
            CREATE TRIGGER IF NOT EXISTS after_admin_insert
            AFTER INSERT ON admin
            FOR EACH ROW
            BEGIN
                INSERT INTO current_session (id, lastlogin, level, ip, active)
                VALUES (NEW.id, NULL, 3, ip, active);
            END;
        '''
    ))
    mysql.session.execute(text(
        '''
            CREATE TRIGGER IF NOT EXISTS after_proff_insert
            AFTER INSERT ON proff
            FOR EACH ROW
            BEGIN
                INSERT INTO current_session (id, lastlogin, level, ip, active)
                VALUES (NEW.p_id, NULL, 2, ip, active);
            END;
        '''
    ))
    mysql.session.execute(text(
        '''
            CREATE TRIGGER IF NOT EXISTS after_student_insert
            AFTER INSERT ON student
            FOR EACH ROW
            BEGIN
                INSERT INTO current_session (id, lastlogin, level, ip, active)
                VALUES (NEW.s_id, NULL, 1, ip, active);
            END;
        '''
    ))

def add_procedures():
    mysql.session.execute(text(
        '''
            CREATE PROCEDURE IF NOT EXISTS after_current_update(IN user_id INTEGER, IN user_level INTEGER, IN user_ip VARCHAR(255))
            BEGIN
                UPDATE current_session 
                SET active=FALSE 
                WHERE ip = user_ip AND (id != user_id OR level != user_level);
            END;
        '''
    ))
    mysql.session.execute(text(
        '''
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
        '''
    ))

    mysql.session.execute(text(
        '''
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
        '''
    ))
    mysql.session.commit()

with app.app_context():
    dropall()
    create_tables()
    add_triggers()    
    add_procedures()
    mysql.session.execute(text(
        '''
            INSERT INTO admin(username, password) VALUES('admin', 'admin');
        '''
    ))
    mysql.session.execute(text(
        '''
            INSERT INTO dept(d_name) VALUES('CSE');
        '''
    ))
    mysql.session.execute(text(
        '''
            INSERT INTO dept(d_name) VALUES('MNC');
        '''
    ))
    mysql.session.execute(text(
        '''
            INSERT INTO dept(d_name) VALUES('ELE');
        '''
    ))
    mysql.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/AddSession', methods=['POST'])
def sessionAdd():
    #check if current user has level 3
    ip = request.json['ip']
    name = request.json['name']
    user_check = mysql.session.execute(text("SELECT id FROM current_session WHERE ip=:ip AND active=TRUE AND level=3"), {'ip': ip})
    if user_check.rowcount == 1:
        # The user has level == 3, proceed with the session insert
        result = mysql.session.execute(text("INSERT INTO session(s_name, active) VALUES(:name, FALSE)"), {'name': name})
        if result.rowcount == 1:
            mysql.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'failed'})
    else:
        return jsonify({'status': 'permission denied'})
    
@app.route('/api/SetSession', methods=['POST'])
def sessionSet():
    # Check if the current user has level 3
    ip = request.json['ip']
    name = request.json['name']
    
    result = mysql.session.execute(text(
        '''
        UPDATE session
        SET active = CASE 
            WHEN (SELECT level FROM current_session WHERE ip=:ip AND active=TRUE) = 3 THEN 
                CASE 
                    WHEN s_name = :name THEN TRUE
                    ELSE FALSE
                END
            ELSE FALSE
        END
        WHERE TRUE
        '''
    ), {'ip': ip, 'name': name})
    mysql.session.commit()

    if result.rowcount > 0:
        mysql.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'permission denied'})


@app.route('/api/LoginAdmin', methods=['POST'])
def adminLogin():
    username = request.json['username']
    password = request.json['password']
    ip = request.json['ip']
    result = mysql.session.execute(text("SELECT * FROM admin WHERE username=:username AND password=:password"), {'username': username, 'password': password})
    if result.rowcount == 1:
        user_id = result.fetchone()[0]
        mysql.session.execute(text("UPDATE current_session SET lastlogin=NOW(), ip=:ip, active=TRUE WHERE id=:id and level=3"), {'id': user_id, 'ip': ip})
        mysql.session.execute(text("CALL after_current_update(:id, :level, :ip)"), {'id': user_id, 'level': 3, 'ip': ip})
        mysql.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'failed'})
    
@app.route('/api/LoginProff', methods=['POST'])
def proffLogin():
    username = request.json['username']
    password = request.json['password']
    ip = request.json['ip']
    result = mysql.session.execute(text("SELECT * FROM proff WHERE p_email=:username AND p_password=:password"), {'username': username, 'password': password})
    if result.rowcount == 1:
        user_id = result.fetchone()[0]
        mysql.session.execute(text("UPDATE current_session SET lastlogin=NOW(), ip=:ip, active=TRUE WHERE id=:id and level=2"), {'id': user_id, 'ip': ip})
        mysql.session.execute(text("CALL after_current_update(:id, :level, :ip)"), {'id': user_id, 'level': 2, 'ip': ip})
        mysql.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'failed'})

@app.route('/api/AddProff', methods=['POST'])
def proffAdd():
    name = request.json['name']
    password = request.json['password']
    dept = request.json['dept']
    email = request.json['email']
    ip = request.json['ip']

    # Check if the current user has level == 3
    user_check = mysql.session.execute(text("SELECT id FROM current_session WHERE ip=:ip AND active=TRUE AND level=3"), {'ip': ip})

    if user_check.rowcount == 1:
        # The user has level == 3, proceed with the proff insert
        result = mysql.session.execute(text("INSERT INTO proff(p_name, p_email, p_password, d_id) VALUES(:name, :email, :password, :dept)"), {'name': name,'email': email , 'password': password, 'dept': dept})
        
        if result.rowcount == 1:
            mysql.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'failed'})
    else:
        return jsonify({'status': 'permission denied'})
    
@app.route('/api/AddCourse', methods=['POST'])
def courseAdd():
    name = request.json['name']
    cred = request.json['cred']
    ip = request.json['ip']

    # Check if the current user has level == 2 and an active session is set
    result = mysql.session.execute(
        text('''
                CALL add_course(:ip, :name, :cred)
            '''
        ),
        {'ip': ip, 'name': name, 'cred': cred}
    )
    mysql.session.commit()

    status = result.fetchone()[0]
    return jsonify({'status': status})


@app.route('/api/AddStudentCourse', methods=['POST'])
def student_add_course():
    ip = request.json['ip']
    course_id = request.json['course_id']
    year = request.json['year']
    degree = request.json['degree']
    dept = request.json['dept']

    result = mysql.session.execute(
        text("CALL student_add_course(:ip, :course_id, :year, :degree, :dept)"),
        {'ip': ip, 'course_id': course_id, 'year': year, 'degree': degree, 'dept': dept}
    )
    mysql.session.commit()
    status = result.fetchone()[0]

    return jsonify({'status': status})
    
@app.route('/api/LoginStudent', methods=['POST'])
def studentLogin():
    username = request.json['username']
    password = request.json['password']
    ip = request.json['ip']
    result = mysql.session.execute(text("SELECT * FROM student WHERE s_email=:username AND s_password=:password"), {'username': username, 'password': password})
    if result.rowcount == 1:
        user_id = result.fetchone()[0]
        mysql.session.execute(text("UPDATE current_session SET lastlogin=NOW(), ip=:ip, active=TRUE WHERE id=:id and level=1"), {'id': user_id, 'ip': ip})
        mysql.session.execute(text("CALL after_current_update(:id, :level, :ip)"), {'id': user_id, 'level': 1, 'ip': ip})
        mysql.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'failed'})

@app.route('/api/AddStudent', methods=['POST'])
def studentAdd():
    name = request.json['name']
    password = request.json['password']
    year = request.json['year']
    roll = request.json['roll']
    dept = request.json['dept']
    email = request.json['email']
    degree = request.json['degree']
    ip = request.json['ip']

    # Check if the current user has level == 3
    user_check = mysql.session.execute(text("SELECT id FROM current_session WHERE ip=:ip AND active=TRUE AND level=3"), {'ip': ip})

    if user_check.rowcount == 1:
        # The user has level == 3, proceed with the proff insert
        result = mysql.session.execute(text("INSERT INTO student(s_name, s_email, s_roll, s_password, s_degree, s_year, s_dept) VALUES(:name, :email, :roll, :password, :degree, :year, :dept)"), {'name': name,'email': email , 'roll': roll, 'password': password, 'degree': degree, 'year': year, 'dept': dept})
        
        if result.rowcount == 1:
            mysql.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'failed'})
    else:
        return jsonify({'status': 'permission denied'})
    
if __name__ == '__main__':
    app.run(debug=True)