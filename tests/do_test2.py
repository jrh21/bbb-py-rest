from flask import Flask, jsonify, g, request
from sqlite3 import dbapi2 as sqlite3

DATABASE = './database.db'
app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None: db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def find_student(name=''):
    sql = "select * from contacts where id = '%s'" % (name)
    db = get_db()
    rv = db.execute(sql)
    res = rv.fetchall()
    rv.close()
    return res[0]


@app.route('/dev')
def find_user_by_name():
    page = request.args.get('page', default=1, type=str)
    filter = request.args.get('filter', default=1, type=str)
    # student = find_student(_id)
    # # print(student)
    #
    # if student: print(2222222)
    print(page)
    print(filter)
    # username=student['username']
    # email=student['email']
    return page

if __name__ == '__main__': app.run(debug=True)
