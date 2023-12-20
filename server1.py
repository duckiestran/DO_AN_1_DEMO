import flask
from server2 import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgre@localhost:5432/Information"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app) #liên kết db với ứng dụng flask


#Tạo bảng trong SQL 
def main():
    db.create_all()


if __name__ == "__main__":
    with app.app_context():  #cho phép nhà phát triển tương tác với flask thông qua dòng lệnh cmd
        main()

