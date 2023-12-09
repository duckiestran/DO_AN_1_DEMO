from server2 import *

from flask import Flask, request, render_template,url_for,redirect,request

from sqlalchemy.exc import DataError

from sqlalchemy import Integer, cast




app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432/Information"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)
db.init_app(app)

#____________________________________

#trang đăng nhập
@app.route("/timtro365") 
def home():
    return render_template("index.html")
 
#trang đăng ký
@app.route("/signup")
def signup():
    return render_template("signup.html")

#thông báo đăng ký tài khoản thành công 
@app.route("/success")
def timtro():
    return render_template("success.html")

#trang chủ web
@app.route("/homepage")
def homepage():
    return render_template("home.html")

#thông tin tài khoản
@app.route("/profile")
def profile():
    return render_template("profile.html")

#tìm người ở ghép
@app.route("/roommate")
def roommate():
    return render_template("roommate.html")

#test
@app.route("/test")
def test():
    return render_template("test.html")




#tìm kiếm nhà trọ theo khu vực người dùng chọn
@app.route('/search')  
def search():
    hostel = Hostel.query.all()
    return render_template("search.html", Hostel=hostel)


#______________________________________
#Thông tin đăng ký mới 
@app.route("/Signup")  
def Signup():   
    number_phone = request.args.get("phone")
    password = request.args.get("password")#request về password bên signup
    name = request.args.get("name")
    birth = request.args.get("birth")
        
        
    name_signup = SignUp(number_phone=number_phone, password=password,name=name,birth=birth) #pass ở đầu là var bên Create_tableSQL, pass còn lại là var bên này
    db.session.add(name_signup)  
    db.session.commit()

    return render_template("success.html")

#_________________________________________
#Đăng nhập vào web
#check tài khoản mật khẩu để đăng nhập
@app.route("/login", methods=["GET","POST"]) #GET là yêu cầu dữ liệu từ bên sever thông qua URL của web/POST là gửi dữ liệu từ client lên sever  
                                              
def login():
    try:
        if request.method == "POST":
            number_phone = request.form.get("phone")
            password = request.form.get("password")
        
            user = SignUp.query.filter_by(number_phone=number_phone).first() #check tài khoản mật khẩu trong database
            if user and user.password == password:
                return redirect(url_for("homepage")) #đăng nhập thành công thì return về trang chủ
            else:
                return render_template("index.html")
        else:
            return render_template("index.html")
        
    except DataError:
        return redirect(url_for("timtro365")) #nhập chữ vào số điện thoại sẽ return về lại trang đăng nhập


#_________________________________________
#Tìm kiếm nhà trọ theo khu vực
@app.route("/result", methods=["get"])
def result():
    # Nhận thông tin từ form
    location = request.args.get("location")
    price_range = request.args.get("price")
    acreage_range = request.args.get("acreage")

    print("location")
    print(location)

    print("price")
    print(price_range)

    print("acreage")
    print(acreage_range)

    # Xử lý truy vấn
    query = Hostel.query

    if location:
        search_location = f"%{location}%"
        print("search_location")
        print(search_location)
        query = query.filter(Hostel.location.like(search_location))
    print(query)
    
    if price_range:
        price_range = price_range.replace(",", "").strip()
            
        if "-" in price_range:
            min_price, max_price = map(str, price_range.split("-"))
            query = query.filter(cast(Hostel.price, Integer).between(min_price, max_price))
        else:
            # Xử lý khi không có dấu "-"
            min_price, max_price = 0, 0


    # Sử dụng cast để chuyển đổi kiểu dữ liệu của cột price
    query = query.filter(cast(Hostel.price, Integer).between(min_price, max_price))
    print(query)
     

    if acreage_range:
        acreage_range = acreage_range.replace(",", "").strip()
        
        if "-" in acreage_range:
            min_acreage, max_acreage = map(str, acreage_range.split("-"))
            query = query.filter(cast(Hostel.acreage, Integer).between(min_acreage, max_acreage))
        else:
            # Xử lý khi không có dấu "-"
            min_acreage, max_acreage = 0, 0

    # Sử dụng cast để chuyển đổi kiểu dữ liệu của cột acreage
    query = query.filter(cast(Hostel.acreage, Integer).between(min_acreage, max_acreage))
    print(query)
    
   # Thực hiện truy vấn
    result_hostels = query.all()
    print("result_hostels")
    print(result_hostels)
    
    return render_template("result.html", hostels=result_hostels)
    
    

@app.route("/addPost")
def addPost():
    return render_template("add-posts.html")


@app.route("/addPostSuccess")
def addPostSuccess():
    key_id = request.args.get("key_id")
    title = request.args.get("title")
    price = request.args.get("price")
    acreage = request.args.get("acreage")
    location = request.args.get("location")

    room = Hostel(title=title, price=price, acreage=acreage, location=location)
    db.session.add(room)
    db.session.commit()
    return render_template("add-posts-success.html")


@app.route("/showPostsForRent")
def showPostsForRent():
    hos = Hostel.query.all()
    return render_template("show-all-posts.html", hostels=hos)


@app.route("/delPosts")
def delPosts():
    return render_template("del-posts.html")


@app.route("/delPostsSuccess")
def delPostsSuccess():
    key_id = request.args.get("key_id")
    exists = False
    exists = Hostel.query.filter_by(key_id=key_id).scalar() is not None
    while exists:
        obj = Hostel.query.filter_by(key_id=key_id).first()
        db.session.delete(obj)
        db.session.commit()
        return render_template("del-Posts-success.html")
    else:
        return render_template('invalidkey_id.html')


@app.route("/updatePosts")
def updatePosts():
    return render_template("update-posts.html")


@app.route("/updatePostsSuccess")
def updatePostsSuccess():
    key_id = request.args.get("key_id")
    title = request.args.get("title")
    price = request.args.get("price")
    acreage = request.args.get("acreage")
    location = request.args.get("location")

    exists = Hostel.query.filter_by(key_id=key_id).scalar()
    while exists:
        obj_change = Hostel.query.filter_by(key_id=key_id).update(dict(title=title, price=price, acreage=acreage, location=location))
        db.session.commit()
        return render_template("update-posts-success.html")
    else:
        return render_template("invalidkey_id.html")