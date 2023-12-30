from flask import Flask , render_template , request , redirect, url_for
import sqlite3

con = sqlite3.connect("zoo.db", check_same_thread=False)
cur = con.cursor()
app = Flask(__name__)

cur.execute("""
    CREATE TABLE IF NOT EXISTS zoo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        animal TEXT,
        age INTEGER,
        category TEXT,
        picture TEXT
    )
""")
con.commit()


@app.route("/")
def home():
    cur.execute("SELECT * , id FROM zoo")
    zoo = cur.fetchall()
    return render_template('home.html', zoo=zoo)

@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # Retrieve form data
        animal = request.form.get("animal")
        age = request.form.get("age")
        category = request.form.get("category")
        picture = request.form.get("picture")

        # Insert data into the 'zoo' table
        cur.execute("INSERT INTO zoo (animal, age, category, picture) VALUES (?, ?, ?, ?)", (animal, age, category, picture))
        con.commit()

        # Redirect to the home page after adding the animal
        return redirect(url_for('home'))
    else:
        return render_template('add.html')

@app.route("/update/<int:zoo_id>", methods=["GET", "POST"])
def update(zoo_id):
    if request.method == "POST":
        # Retrieve form data
        animal = request.form.get("animal")
        age = request.form.get("age")
        category = request.form.get("category")
        picture = request.form.get("picture")

        # Update data in the 'zoo' table based on the ID
        cur.execute("UPDATE zoo SET animal=?, age=?, category=?, picture=? WHERE id=?", (animal, age, category, picture, zoo_id))
        con.commit()

        # Redirect to the home page after updating the animal
        return redirect(url_for('home'))
    else:
        # Retrieve the current data of the animal based on the ID
        cur.execute("SELECT * FROM zoo WHERE id=?", (zoo_id,))
        animal_data = cur.fetchone()

        # Render the update template with the current data
        return render_template('update.html', animal_data=animal_data)

    
   

@app.route("/remove/<int:zoo_id>", methods=['POST'])
def remove(zoo_id):
    if request.method == 'POST':
    
        # Remove the car from the 'car' table based on the brand
        cur.execute("DELETE FROM zoo WHERE id = ?", (zoo_id,))
        con.commit()

        # Redirect to the home page after removing the car
        return redirect(url_for('home'))


if __name__=='__main__':
    app.run(debug=True)