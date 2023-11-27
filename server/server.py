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
    try:
        with open('drop.sql', 'r') as f:
            queries = f.read().split(';')
            for query in queries:
                mysql.session.execute(text(query))
            mysql.session.commit()
    except Exception as e:
        print(e)

def create_tables():
    try:
        with open('schema.sql', 'r') as f:
            queries = f.read().split(';')
            for query in queries:
                mysql.session.execute(text(query))
            mysql.session.commit()
    except Exception as e:
        print(e)

def add_triggers():
    try:
        with open('trigger.sql', 'r') as f:
            queries = f.read().split('/')
            for query in queries:
                mysql.session.execute(text(query))
            mysql.session.commit()
    except Exception as e:
        print(e)

def add_procedures():
    try:
        with open('procedure.sql', 'r') as f:
            queries = f.read().split('/')
            for query in queries:
                mysql.session.execute(text(query))
            mysql.session.commit()
    except Exception as e:
        print(e)

with app.app_context():
    dropall()
    create_tables()
    add_triggers()    
    add_procedures()
    try:
        with open('test.sql', 'r') as f:
            queries = f.read().split('/')
            for query in queries:
                mysql.session.execute(text(query))
            mysql.session.commit()
    except Exception as e:
        print(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/AddSession', methods=['POST'])
def sessionAdd():
    #check if current user has level 3
    ip = request.json['ip']
    name = request.json['name']
    sql_query = "CALL session_add(:ip, :name)"
    params = {
        'ip': ip,
        'name': name
    }

    result = mysql.session.execute(text(sql_query), params)
    mysql.session.commit()
    status = result.fetchone()[0]
    return jsonify({'status': status})
    
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
    sql_query = "CALL proff_login(:username, :password, :ip)"
    params = {
        'username': username,
        'password': password,
        'ip': ip
    }

    result = mysql.session.execute(text(sql_query), params)
    mysql.session.commit()
    status = result.fetchone()[0]
    return jsonify({'status': status})

@app.route('/api/AddProff', methods=['POST'])
def proffAdd():
    name = request.json['name']
    password = request.json['password']
    dept = request.json['dept']
    email = request.json['email']
    ip = request.json['ip']

    sql_query = "CALL proff_add(:name, :password, :dept, :email, :ip)"
    params = {
        'name': name,
        'password': password,
        'dept': dept,
        'email': email,
        'ip': ip
    }

    result = mysql.session.execute(text(sql_query), params)
    mysql.session.commit()
    status = result.fetchone()[0]
    return jsonify({'status': status})
    
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

@app.route('/api/GetCourses', methods=['GET'])
def getCourses():
    result = mysql.session.execute(text(
        '''
            SELECT c_id, c_name, c_cred, p_name, s_name
            FROM course
            INNER JOIN proff ON course.p_id = proff.p_id
            INNER JOIN session ON course.c_session = session.s_id
        '''
    ))
    mysql.session.commit()
    if result.rowcount > 0:
        results = result.fetchall()
        results = [tuple(row) for row in results]
        return jsonify(results)
    else:
        return jsonify([])
    
@app.route('/api/LoginStudent', methods=['POST'])
def studentLogin():
    username = request.json['username']
    password = request.json['password']
    ip = request.json['ip']
    sql_query = "CALL student_login(:username, :password, :ip)"
    params = {
        'username': username,
        'password': password,
        'ip': ip
    }

    result = mysql.session.execute(text(sql_query), params)
    mysql.session.commit()
    status = result.fetchone()[0]
    return jsonify({'status': status})

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

    sql_query = "CALL student_add(:name, :password, :year, :roll, :dept, :email, :degree, :ip)"
    params = {
        'name': name,
        'password': password,
        'year': year,
        'roll': roll,
        'dept': dept,
        'email': email,
        'degree': degree,
        'ip': ip
    }

    result = mysql.session.execute(text(sql_query), params)
    mysql.session.commit()
    status = result.fetchone()[0]
    return jsonify({'status': status})
    
if __name__ == '__main__':
    app.run(debug=True)