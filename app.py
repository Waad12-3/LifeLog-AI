from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
import csv
from models import db, Entry

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lifelog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/download/txt')
def download_txt():
    entries = Entry.query.order_by(Entry.date.desc()).all()
    output = "\n\n".join(f"[{e.date.strftime('%Y-%m-%d %H:%M')}] {e.mood}\n{e.content}" for e in entries
    )
    response = make_response(output)
    response.headers["Content-Disposition"] = "attachment; filename=journal.txt"
    response.mimetype = "text/plain"
    return response

@app.route('/download/csv')
def download_csv():
    entries = Entry.query.order_by(Entry.date.desc()).all()
    output = []
    for e in entries:
        output.append([e.date.strftime('%Y-%m-%d %H:%M'), e.mood, e.content])

    si = "\n".join([",".join(map(lambda x: f'"{x}"', row)) for row in output])

    response = make_response(si)
    response.headers["Content-Disposition"] = "attachment; filename=journal.csv"
    return response

@app.route('/history-data')
def history_data():
    mood = request.args.get('mood')
    q = request.args.get('q')
    query = Entry.query
    if mood:
        query = query.filter_by(mood=mood)
    if q:
        query = query.filter(Entry.content.ilike(f"%{q}%"))
    entries = query.order_by(Entry.date.desc()).all()
    return jsonify([
        {
            'content' : e.content,
            'date' : e.date.strftime('%Y-%m-%d %H:%M'),
            'mood' : e.mood
        }
        for e in entries
    ])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/entry', methods=['GET', 'POST'])
def entry():
    if request.method == 'POST':
        content = request.form['content']
        mood = request.form['mood']
        if content:
            new_entry = Entry(content=content, mood=mood)
            db.session.add(new_entry)
            db.session.commit()
            return redirect('/history')
    return render_template('entry.html')

@app.route('/history')
def history():
    mood_filter = request.args.get('mood')
    search_query = request.args.get('q')

    query = Entry.query
    if mood_filter:
        query = query.filter_by(mood=mood_filter)
    if search_query:
        query = query.filter(Entry.content.ilike(f"%{search_query}%"))

    entries = query.order_by(Entry.date.desc()).all()
    return render_template('history.html', entries=entries, mood_filter=mood_filter, search_query=search_query)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)