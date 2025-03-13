from flask import Flask,render_template,url_for,request,jsonify,redirect
import joblib  
import mysql.connector as con 


app=Flask(__name__)

model1=joblib.load("XGBClassifier.lb")
model2=joblib.load("XGBRegressor.lb")
model3=joblib.load("GradientBoostingRegressor.lb")

@app.route("/")
def home():
    return render_template("form.html")

@app.route("/form_data",methods=["GET","POST"])
def form_data():
    if request.method=="POST":
        dep=request.form["dep"]
        ed=request.form["ed"]
        se=request.form["se"]
        inn=request.form["inn"]
        la=request.form["la"]
        lt=request.form["lt"]
        cibil=request.form["cibil"]
        ra=request.form["ra"]
        ca=request.form["ca"]
        lua=request.form["lua"]
        ba=request.form["ba"]
        
        unseen_data_m1 = [[int(ed), int(se), int(dep), int(inn), int(la),
                int(lt), int(cibil), int(ra), int(ca), int(lua), int(ba)]]
        
        unseen_data_m2 = [[int(ed), int(se), int(dep), int(inn),
                int(lt), int(cibil), int(ra), int(ca), int(lua), int(ba)]]

        pred1 = model1.predict(unseen_data_m1)
        pred1 = pred1.ravel()
        ls=int(pred1[0])
        # if int(pred[0])==0:
        #     return "Loan Approved"
        # else :
        #     return "Loan Rejected"
        
        pred2 = model2.predict(unseen_data_m2)
        pred2 = pred2.ravel()
        lap=round(int(pred2[0],2)
        
        #tuple
        main_data = (int(ed), int(se), int(dep), int(inn), int(la),
                int(lt), int(cibil), int(ra), int(ca), int(lua), int(ba),ls,lap)
        
        #database work
        #mysql connection work 
        conn=con.connect(
            host="localhost",
            user="root",
            password="",
            database="loan"
        )
        #create the cursor object 
        cursor = conn.cursor()
        
        Qurey="insert into prediction(ed,se,dep,inn,la,lt,cibil,ra,ca,lua,ba,p,lap) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(Qurey,main_data)
        
        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()
        return redirect(url_for("dashboard"))

@app.route('/dashboard')
def dashboard():
    # Connect to the database and fetch candidate data
    conn = con.connect(
        host="localhost",
        user="root",
        password="",
        database="loan"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select * from prediction where id=(select max(id) from prediction)")
    prediction = cursor.fetchall()
    cursor.close()
    conn.close()

    # Render the template and pass the candidates data to it
    return render_template('dashboard.html',prediction=prediction)



if "__main__"==__name__:
    app.run(debug=True)