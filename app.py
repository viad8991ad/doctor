from flask import Flask, render_template, request

from sqlite3 import connect

from repository import init

app = Flask(__name__)
db = "resources/history.db"
init(db)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/records', methods=['POST', 'GET'])
def records():
    with connect(db) as con:
        cur = con.cursor()
        cur.execute("SELECT fio, birthday, snils, polis, address, phone, data FROM register")
        register = cur.fetchall()
    return render_template('records.html', register=register)


@app.route('/card/<patient_id>', methods=['POST', 'GET'])
def card(patient_id):
    with connect(db) as con:
        cur = con.cursor()
        cur.execute("""
            SELECT r.id, r.fio, r.birthday, d.diagnosis, d.complaint, d.treatment 
            FROM register AS r 
                LEFT JOIN diagnosis AS d ON r.id = d.register_id""")
        patients = [[v if v is not None else "" for v in list_of_list] for list_of_list in cur.fetchall()]
        current = ["", "", ""]
        for x in patients:
            if str(x[0]) == patient_id:
                current = x
                break
    if request.method == 'POST':
        diagnosis = request.form['diagnosis']
        complaint = request.form['complaint']
        treatment = request.form['treatment']
        with connect(db) as con:
            cur = con.cursor()
            cur.execute("SELECT register_id FROM diagnosis WHERE register_id = ?", (patient_id,))
            if cur.fetchone() is None:
                cur.execute("INSERT INTO diagnosis VALUES (?, ?, ?, ?)", (patient_id, diagnosis, complaint, treatment))
            else:
                cur.execute(
                    """UPDATE diagnosis SET diagnosis = ?, complaint = ?, treatment = ? WHERE register_id = ?""",
                    (request.form['diagnosis'], request.form['complaint'], request.form['treatment'], patient_id)
                )
            con.commit()
    return render_template('card.html', patients=patients, current=current)


if __name__ == '__main__':
    app.run()
