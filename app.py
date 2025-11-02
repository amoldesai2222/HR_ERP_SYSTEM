from flask import Flask, render_template,request, redirect, session
from flask_mysqldb import MySQL


app = Flask(__name__)

app.secret_key = "AMOL"
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="hr_erp_db"

con=MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template ("aboutus.html")

@app.route("/admin")
def admin():
    return render_template ("adminlogin.html")

@app.route("/contact")
def contact():
    return render_template ("contactus.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    username = request.form.get("txtusername")
    password = request.form.get("txtpassword")

    if username == "amoldesai" and password == "Amol@123":
        return render_template("admin_dashboard.html")
    else:
        msg = "invalid username or password"
        return render_template ("adminlogin.html", message=msg)
    


       


@app.route("/addemp")
def addemp():
    return render_template("admin_addemp.html")

@app.route("/showemp")
def showemp():
     
    cur = con.connection.cursor()
    cur.execute("SELECT empid,name,emailid FROM registration")
    emplist= cur.fetchall()


    return render_template("admin_showemp.html",recordlist=emplist)

@app.route("/searchemp")
def searchemp():
    
    return render_template("admin_searchemp.html")




@app.route("/save", methods=["GET" ,"POST"])
def save():
    i = request.form.get("txtEmpId")
    n = request.form.get("txtName")
    e = request.form.get("txtEmail")
    m = request.form.get("txtMobile")
    d = request.form.get("txtDesignatin")
    s = request.form.get("txtSalary")

    cur = con.connection.cursor()
    cur.execute(
        "INSERT INTO registration(empid,name, emailid, mobileno, designation, salary) VALUES (%s, %s, %s, %s, %s, %s)",
        (i, n, e, m, d, s),
    )
    con.connection.commit()
    cur.close()

    return render_template("admin_regemp.html")


@app.route("/empprofile")
def empprofile():
    id = request.args.get("eid")
    cur = con.connection.cursor()
    cur.execute("SELECT * FROM hr_erp_db.registration WHERE empid = %s", (id,))
    rl = cur.fetchall()
    return render_template("admin_empprofile.html", emplist=rl)

@app.route("/empupdate", methods=["POST"])
def empupdate():
    i = request.form.get("txtEmpId")
    n = request.form.get("txtName")
    e = request.form.get("txtEmail")
    m = request.form.get("txtMobile")
    d = request.form.get("txtDesignation")  
    s = request.form.get("txtSalary")

    cur = con.connection.cursor()
    cur.execute("""
        UPDATE registration
        SET name=%s, emailid=%s, mobileno=%s, designation=%s, salary=%s
        WHERE empid=%s
    """, (n, e, m, d, s, i))
    
    con.connection.commit()  
    cur.close()

    return render_template("admin_update_success.html")


@app.route("/searchprocess", methods=["POST"])
def searchprocess():
    n = request.form['txtname']
    print("Searching for:", n)

    cur = con.connection.cursor()
    query = "SELECT * FROM registration WHERE LOWER(name) LIKE LOWER(%s)"
    cur.execute(query, ('%' + n + '%',))
    emplist = cur.fetchall()
    print("Results:", emplist)
    cur.close()

    return render_template("admin_searchprocessemp.html", emplist=emplist)


@app.route("/logout")
def logout():
    return render_template("adminlogin.html")





if __name__ == '__main__':
    app.run(debug=True)


