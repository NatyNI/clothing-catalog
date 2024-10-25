import os
from dotenv import load_dotenv
import mysql.connector
from flask import Flask, render_template, request, send_from_directory, jsonify


app = Flask (__name__)

try:

    load_dotenv()
    connection = mysql.connector.connect(
        host="localhost",
        user = os.getenv("my_user"),
        password = os.getenv("my_password"),
        database = os.getenv("my_database")
    )
    print ("Connected to database succesfully")

except mysql.connector.Error as err:
    print("Cannot connect to database")

@app.route("/css/<path:filename>")
def send_css(filename):
    return send_from_directory("static/css", filename)

class Catalog():
    def __init__(self, nr, tip, brand, description):
        self.nr=nr
        self.tip=tip
        self.brand=brand
        self.description=description



@app.route("/")
def home():

    connection.connect()
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM catalog")

    result_query=cursor.fetchall()
    values=[]
    for column in result_query:
        catalog_object=Catalog(column[0], column[1],column[2],column[3],)
        values.append(catalog_object)

    return render_template ("home.html", result= values)

@app.route("/addclothing", methods=["GET", "POST"])
def add_clothing():
    if request.method == "GET":
        return render_template("addtocatalog.html")
    elif request.method == "POST":
        post_object=Catalog(
            nr= request.form.get("Nr"),
            tip= request.form.get("Tip"),
            brand= request.form.get("Brand"),
            description= request.form.get("Description")
        )
        connection.connect()
        cursor=connection.cursor()
        query="""INSERT INTO catalog (Nr, Tip, Brand, Description)
                 VALUES (%s, %s, %s, %s)"""
        cursor.execute(query,(post_object.nr, post_object.tip,
                               post_object.brand, post_object.description))
        connection.commit()
        connection.close()
        cursor.close()
        return "The clothing has been added to the catalog"

@app.route("/description/<tipclothing>")
def description(tipclothing):

    connection.connect()
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM catalog WHERE Tip = %s", (tipclothing,))
    value= cursor.fetchone()
    result=[]
    val_object=Catalog(value[0], value[1], value[2], value[3])
    result.append(val_object)

    connection.close()
    cursor.close()
    return render_template("description.html", values=result)

@app.route("/search")
def serach():

    return render_template("search.html")

@app.route("/searchclothing")
def search_clothing():

    brand= request.args.get("Brand")
    connection.connect()
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM catalog")
    brand_name=[]
    query_result=cursor.fetchall()
    for name in query_result:
        brand_name.append(name[2])

    if brand in brand_name:
        cursor.execute("SELECT * FROM catalog WHERE Brand=%s", (brand,))
        clothing=cursor.fetchone()
        print(clothing)
        return (f"This is your clothing from catalog:<br><br>"
                f"In stock: {clothing[0]} <br>" 
                f"Tip: {clothing[1]} <br>" 
                f"Brand: {clothing[2]}")
    else:
        return "We can t find any clothing at this brand"

if __name__ =="__main__":
    app.run(port = 2000)
