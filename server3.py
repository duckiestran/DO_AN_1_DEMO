from psycopg2 import IntegrityError
from server2 import *

from flask import Flask, request, render_template,url_for,redirect,request

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.exc import DataError

from sqlalchemy import Integer, cast



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgre@localhost:5432/Information"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)


#____________________________________

#Admin /Xong
@app.route("/admin") 
def admin():
    return render_template("admin.html")

@app.route("/admin2") 
def admin2():
    return render_template("control.html")

#trang đăng nhập / Xong
@app.route("/timtro365") 
def home():
    return render_template("index.html")
 
#trang đăng ký /Xong
@app.route("/signup")
def signup():
    return render_template("signup.html")

#thông báo đăng ký tài khoản thành công /Xong
@app.route("/success")
def timtro():
    return render_template("success.html")

#tìm kiếm nhà trọ theo khu vực người dùng chọn /Xong
@app.route('/search')  
def search():
    hostel = Hostel.query.all()
    return render_template("search.html", Hostel=hostel)

#trang chủ web /Xong
@app.route("/homepage")
def homepage():
    return render_template("home.html")


#thông tin tài khoản
@app.route("/profile")
def profile():
    return render_template("profile.html")


#test
@app.route("/test")
def test():
    return render_template("test.html")




#______________________________________
#Tài khoản admin / xong
@app.route("/login_ad", methods=["GET","POST"])
                                              
def login_ad():
    try:
        if request.method == "POST":
            phone_admin = request.form.get("phone_admin")
            pass_admin = request.form.get("pass_admin")
            
        
            ad = Admin.query.filter_by(phone_admin=phone_admin).first() #check tài khoản mật khẩu trong database
            if ad and ad.pass_admin == pass_admin:
                return redirect(url_for("admin2")) #đăng nhập thành công thì return về trang chủ
            else:
                return render_template("admin.html")
        else:
            return render_template("admin.html")
        
    except DataError:
        return redirect(url_for("admin")) #nhập chữ vào số điện thoại sẽ return về lại trang đăng nhập

#______________________________________
#Thông tin đăng ký mới / xong
@app.route("/Signup")  
def Signup():
    try:
        number_phone = request.args.get("phone")
        password = request.args.get("password")#request về password bên signup
        name = request.args.get("name")
        birth = request.args.get("birth")
            
            
        name_signup = SignUp(number_phone=number_phone, password=password,name=name,birth=birth) #pass ở đầu là var bên Create_tableSQL, pass còn lại là var bên này
        db.session.add(name_signup)  
        db.session.commit()

        return render_template("success.html")
    except IntegrityError:
        return "Tài khoản đã tồn tại"

#_________________________________________
#Đăng nhập vào web / xong
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
#Tìm kiếm nhà trọ theo khu vực / xong
@app.route("/result", methods=["get"])
def result():

    # Nhận thông tin từ form bên search.html
    location = request.args.get("location")
    price_range = request.args.get("price")
    acreage_range = request.args.get("acreage")

    # Xử lý truy vấn
    query = Hostel.query

    #khu vực
    if location:
        search_location = f"%{location}%"
        query = query.filter(Hostel.location.like(search_location))
    
    #Giá cả
    if price_range:
        price_range = price_range.replace(",", "").strip()
            
        if "-" in price_range:
            min_price, max_price = map(str, price_range.split("-"))
            query = query.filter(cast(Hostel.price, Integer).between(min_price, max_price))
        else:
            min_price, max_price = 0, 0 # Xử lý khi không có dấu "-"
    
    query = query.filter(cast(Hostel.price, Integer).between(min_price, max_price)) # Sử dụng cast để chuyển đổi kiểu dữ liệu của cột
    
    #Diện tích
    if acreage_range:
        acreage_range = acreage_range.replace(",", "").strip()
        
        if "-" in acreage_range:
            min_acreage, max_acreage = map(str, acreage_range.split("-"))
            query = query.filter(cast(Hostel.acreage, Integer).between(min_acreage, max_acreage))
        else:    
            min_acreage, max_acreage = 0, 0

    query = query.filter(cast(Hostel.acreage, Integer).between(min_acreage, max_acreage))
    

   # Thực hiện truy vấn
    result_hostels = query.all()
    return render_template("result.html", hostels=result_hostels)

#___________________________________________________________
#Tìm kiếm người dùng / xong
@app.route("/InformationSearch")
def InformationSearch():
    name = request.args.get("name")
    number_phone = request.args.get("number_phone")

    #Xử lý truy vấn
    Search_Users = SignUp.query

    #Tìm kiếm bằng tên or số điện thoại
    if name:
        search_name = f"%{name}%"
        Search_Users = Search_Users.filter(SignUp.name.like(search_name))
    
    if number_phone:
        number_phone_int = int(number_phone) #đổi kiểu dữ liệu number_phone thành số nguyên
        Search_Users = Search_Users.filter(SignUp.number_phone == number_phone_int)

    search_users = Search_Users.all()
    return render_template("results_InformationSearch.html", Users=search_users)

#______________________________________________
# Đăng bài cho thuê nhà 

@app.route("/rent")
def rent():
    return render_template("rent.html")

@app.route("/post_success")
def post_success():
    key_id = request.args.get("key_id")
    title = request.args.get("title")
    price = request.args.get("price")
    acreage = request.args.get("acreage")
    location = request.args.get("location")


    new_posts = Hostel(title=title, price=price, acreage=acreage, location=location,key_id=key_id) 
    db.session.add(new_posts)  
    db.session.commit()

    return render_template("post_success.html",new_posts=new_posts)


  
#_____________________________________________
#Phân quyền Admin

#Quản lý bài đăng / Xong
@app.route("/showPostsForRent")
def showPostsForRent():
    result_hostels = Hostel.query.all()
    return render_template("show-all-posts.html", hostels=result_hostels)


#xóa bài đăng / xong
@app.route("/delPostsSuccess")
def delPostsSuccess():
    
    key_id = request.args.get("key_id")
    post = Hostel.query.filter_by(key_id=key_id).first_or_404()

    post = db.session.merge(post) #Sử dụng merge để đính kèm lại đối tượng vào phiên hiện tại trước khi thực hiện xóa.
    db.session.delete(post)
    db.session.commit()

    return render_template("del-posts-success.html")


#Tìm kiếm bài đăng  / xong
@app.route("/PostsSearch")
def PostsSearch():
    key_id = request.args.get("key_id")

    if key_id:
        key_id_int = int(key_id)
        posts_search = Hostel.query.filter(Hostel.key_id == key_id_int).all()
    else:
        posts_search = Hostel.query.all()

    return render_template("search_post_id.html", Posts=posts_search)


#Quản lý người dùng / xong
@app.route("/userManagement")
def userManagement():
    users = SignUp.query.all()
    return render_template("user_management.html", users=users)


#Xoá thông tin người dùng / xong
@app.route("/delUserSuccess")
def delUserSuccess():
    try:
        number_phone = request.args.get("number_phone")
        user = SignUp.query.filter_by(number_phone=number_phone).first_or_404()

        user = db.session.merge(user)
        db.session.delete(user)
        db.session.commit()
        return render_template("del-users-success.html")
    except IntegrityError:
        return "Người dùng không tồn tại"


#Update thông tin người dùng / xong
@app.route("/update_profile", methods=["GET", "POST"])
def update_profile():

    if request.method == "POST":
        update = db.session.merge(SignUp.query.get(request.form.get("phone")))
        update.password = request.form["password"]
        update.name = request.form["name"]
        update.birth = request.form["birth"]
        db.session.commit()

        
    return render_template("success_update.html",update=update)



#Tìm người ở ghép
@app.route('/roomate')  
def roomate():
    def_roomate = Roomate.query.all()
    return render_template("roomate.html", Roomate=def_roomate)


#Tìm kiếm nhà trọ theo khu vực 
@app.route("/result", methods=["get"])
def result():

    # Nhận thông tin từ form bên search.html
    location_room = request.args.get("location_room")
    price_range_room = request.args.get("price_room")
    acreage_range_room = request.args.get("acreage_room")

    # Xử lý truy vấn
    query = Roomate.query

    #khu vực
    if location_room:
        search_location_room = f"%{location_room}%"
        query = query.filter(Roomate.location_room.like(search_location_room))
    
    #Giá cả
    if price_range_room:
        price_range_room = price_range_room.replace(",", "").strip()
            
        if "-" in price_range_room:
            min_price, max_price = map(str, price_range_room.split("-"))
            query = query.filter(cast(Hostel.price, Integer).between(min_price, max_price))
        else:
            min_price, max_price = 0, 0 # Xử lý khi không có dấu "-"
    
    query = query.filter(cast(Roomate.price_room, Integer).between(min_price, max_price)) # Sử dụng cast để chuyển đổi kiểu dữ liệu của cột
    
    #Diện tích
    if acreage_range_room:
        acreage_range_room = acreage_range_room.replace(",", "").strip()
        
        if "-" in acreage_range_room:
            min_acreage, max_acreage = map(str, acreage_range_room.split("-"))
            query = query.filter(cast(Roomate.acreage_room, Integer).between(min_acreage, max_acreage))
        else:    
            min_acreage, max_acreage = 0, 0

    query = query.filter(cast(Roomate.acreage_room, Integer).between(min_acreage, max_acreage))
    

   # Thực hiện truy vấn
    result_room = query.all()
    return render_template("result_room.html", rooms=result_room)


#xóa bài đăng / xong
@app.route("/delPostsRoomateSuccess")
def delPostsRoomateSuccess():
    
    id_room = request.args.get("id_room")
    post_roomate = Roomate.query.filter_by(id_room=id_room).first_or_404()

    post_roomate = db.session.merge(post_roomate) #Sử dụng merge để đính kèm lại đối tượng vào phiên hiện tại trước khi thực hiện xóa.
    db.session.delete(post_roomate)
    db.session.commit()

    return render_template("del-posts-success.html")
