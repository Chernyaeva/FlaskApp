from flask import Flask, render_template
from flask import request
from flask import g
from time import time
from werkzeug.exceptions import BadRequest
from blog.views.users import users_app
from blog.views.articles import articles_app
from blog.models.database import db
from blog.views.auth import login_manager, auth_app
import os
from flask_migrate import Migrate
from blog.security import flask_bcrypt
from blog.views.authors import authors_app



app = Flask(__name__)

cfg_name = os.environ.get("CONFIG_NAME") or "DevConfig"
app.config.from_object(f"blog.configs.{cfg_name}")

app.config["SECRET_KEY"] = "abcdefg123456"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

flask_bcrypt.init_app(app)


@app.cli.command("create-users")
def create_users():
    """
    Run in your terminal:
    flask create-users
    > done! created users: <User #2 'james'>
    """
    from blog.models import User
    james = User(username="james", email="james@users.com")

    db.session.add(james)
    db.session.commit()
    
    print("done! created users:", james)
    

@app.cli.command("create-admin")
def create_admin():
    """
    Run in your terminal:
    ➜ flask create-admin
    > created admin: <User #1 'admin'>
    """
    from blog.models import User
    admin = User(username="admin", is_staff=True)
    admin.password = os.environ.get("ADMIN_PASSWORD") or "adminpass"
    db.session.add(admin)
    db.session.commit()
    print("created admin:", admin)



app.register_blueprint(users_app, url_prefix="/users")
app.register_blueprint(articles_app, url_prefix="/articles")
app.register_blueprint(auth_app, url_prefix="/auth")
app.register_blueprint(authors_app, url_prefix="/authors")

login_manager.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/status/", methods=["GET", "POST"])
def custom_status_code():
    if request.method == "GET":
        return """\
        To get response with custom status code
        send request using POST method
        and pass `code` in JSON body / FormData
        """
        print("raw bytes data:", request.data)
    if request.form and "code" in request.form:
        return "code from form", request.form["code"]
    if request.json and "code" in request.json:
        return "code from json", request.json["code"]
    return "", 204

@app.before_request
def process_before_request():
    """
    Sets start_time to `g` object
    """
    g.start_time = time()


@app.after_request
def process_after_request(response):
    """
    adds process time in headers
    """
    if hasattr(g, "start_time"):
        response.headers["process-time"] = time() - g.start_time
    return response


migrate = Migrate(app, db, compare_type=True, render_as_batch=True)