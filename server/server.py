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
                s_password VARCHAR(255) NOT NULL,
                s_degree VARCHAR(255) NOT NULL,
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
                grade INTEGER NOT NULL,
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
            CREATE TRIGGER after_admin_insert
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
            CREATE TRIGGER after_proff_insert
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
            CREATE TRIGGER after_student_insert
            AFTER INSERT ON student
            FOR EACH ROW
            BEGIN
                INSERT INTO current_session (id, lastlogin, level, ip, active)
                VALUES (NEW.s_id, NULL, 1, ip, active);
            END;
        '''
    ))

with app.app_context():
    dropall()
    create_tables()
    add_triggers()    
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

@app.route('/api/LoginAdmin', methods=['POST'])
def adminLogin():
    username = request.json['username']
    password = request.json['password']
    ip = request.json['ip']
    result = mysql.session.execute(text("SELECT * FROM admin WHERE username=:username AND password=:password"), {'username': username, 'password': password})
    if result.rowcount == 1:
        mysql.session.execute(text("UPDATE current_session SET lastlogin=NOW(), ip=:ip, active=TRUE WHERE id=:id and level=3"), {'id': result.fetchone()[0], 'ip': ip})
        mysql.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'failed'})

@app.route('/api/AddProff', methods=['POST'])
def proffAdd():
    name = request.json['name']
    password = request.json['password']
    dept = request.json['dept']
    ip = request.json['ip']

    # Check if the current user has level == 3
    user_check = mysql.session.execute(text("SELECT id FROM current_session WHERE ip=:ip AND active=TRUE AND level=3"), {'ip': ip})

    if user_check.rowcount == 1:
        # The user has level == 3, proceed with the proff insert
        result = mysql.session.execute(text("INSERT INTO proff(p_name, p_password, d_id) VALUES(:name, :password, :dept)"), {'name': name, 'password': password, 'dept': dept})
        
        if result.rowcount == 1:
            mysql.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'failed'})
    else:
        return jsonify({'status': 'permission denied'})

    
if __name__ == '__main__':
    app.run(debug=True)