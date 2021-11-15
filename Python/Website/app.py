from flask import Flask, render_template, request
import datetime
import sqlite3

app = Flask(__name__)



@app.route('/')
def home():
    return render_template("index.html")


@app.route('/addReview')
def addReview():
    return render_template("addReview.html")


@app.route('/getReviews')
def getReviews():
    return render_template("getReviews.html")


@app.route('/showReport')
def showReport():
    ret2 = sqlite3.connect("reviewData.db")
    print("Connected")
    ret2.row_factory = sqlite3.Row
    c2 = ret2.cursor()

    c2.execute("SELECT Restaurant, AVG(Food) AS Food, AVG(Service) as Service, AVG(Ambience) as Ambience, AVG(Price) "
               "as Price, AVG(Rating) as Rating FROM Ratings GROUP BY Restaurant ORDER BY Rating DESC, Restaurant")
    print("Selected")
    rows2 = c2.fetchmany(10)
    return render_template("showReport.html", rows2=rows2)


@app.route('/showReviews')
def showReviews():
    return render_template("showReviews.html")


@app.route('/addrec', methods=['POST'])
def addrec():
    try:
        if request.method == 'POST':
            msg = "Error with "
            valid = True
            un = str(request.form['Username'])
            rest = str(request.form['Restaurant'])
            oa = str(request.form['Rating'])
            rev = str(request.form['Review'])
            dt = datetime.datetime.now()

            food = float(request.form['Food'])
            serv = float(request.form['Service'])
            amb = float(request.form['Ambience'])
            prc = float(request.form['Price'])
            con = sqlite3.connect("reviewData.db")

            if un.isspace() or len(un) == 0:
                valid = False
                msg = msg + " username"

            if rest.isspace() or len(rest) == 0:
                valid = False
                msg = msg + ", restaurant"

            if rev.isspace() or len(rest) == 0:
                valid = False
                msg = msg + ", review"
            if msg == "Error with ":
                msg = "All values inputted correctly."

            if valid:
                # insert data into table
                with sqlite3.connect("reviewData.db") as con:
                    c = con.cursor()
                    c.execute("INSERT INTO Reviews (Username, Restaurant, ReviewTime, Rating, Review) VALUES (?, ?, ?, "
                          "?, ?)", (un, rest, dt, oa, rev))
                    msg += " Able to insert into Reviews."
                    c.execute("INSERT INTO Ratings (Restaurant, Food, Service, Ambience, Price, Rating) VALUES (?, ?, "
                              "?, ?, ?, ?)", (rest, food, serv, amb, prc, oa))
                    msg += " Able to insert into Ratings."
                    con.commit()
    except:
        con.rollback()
        msg = "Error in insertion"

    finally:
        con.close()
        print(msg)
        return render_template("index.html")


@app.route('/fetch', methods=['POST'])
def fetch():
    ret = sqlite3.connect("reviewData.db")
    ret.row_factory = sqlite3.Row

    name = str(request.form['rest'])

    c = ret.cursor()
    c.execute("SELECT * FROM Reviews WHERE Restaurant=?", (name,))
    rows = c.fetchall()
    return render_template("showReviews.html", rows=rows)


if __name__ == '__main__':
    app.run(debug=True)