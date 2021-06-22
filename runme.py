from users.modules import db, app, os
import users.routes

#main function run flask server
if __name__ == "__main__":
    if os.path.exists("/users/usermanagement.db"):
        pass
    else:
        db.create_all()
    app.run(host='0.0.0.0', debug=True)