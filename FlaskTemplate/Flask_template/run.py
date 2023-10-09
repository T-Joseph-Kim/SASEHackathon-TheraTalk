from flaskShell import app, db


PORT = 8000
HOST = '0.0.0.0'
DEBUG = True



if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=DEBUG, host=HOST, port=PORT)