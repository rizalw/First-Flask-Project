from flask import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(20), nullable = False)
    description = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, title, description):
        self.title = title
        self.description = description

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        data_judul = request.form['judul']
        data_deskripsi = request.form['deskripsi']
        input_baru = Todo(data_judul, data_deskripsi)
        try:
            db.session.add(input_baru)
            db.session.commit()
            return redirect('/')
        except:
            return "Upload gagal"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks = tasks)

@app.route("/delete/<int:id>")
def delete(id):
    delete_data = Todo.query.get_or_404(id)
    try:
        db.session.delete(delete_data)
        db.session.commit()
        return redirect("/")
    except:
        return "Terdapat masalah dalam menghapus data"

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    update_data = Todo.query.get_or_404(id)
    if request.method == "POST":
        update_data.title = request.form["judul"]
        update_data.description = request.form["deskripsi"]
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "Terdapat masalah dalam mengupdate data"
    else:
        return render_template("update.html", tasks = update_data)

if __name__ == "__main__":
    app.run(debug=True)