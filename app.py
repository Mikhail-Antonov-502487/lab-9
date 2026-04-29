from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модель БД: game, year
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    games = Game.query.all()
    return render_template('index.html', games=games)

@app.route('/add', methods=['POST'])
def add_game():
    game_name = request.form.get('game')
    year = request.form.get('year')
    
    if game_name and year:
        try:
            year = int(year)
            new_game = Game(game=game_name, year=year)
            db.session.add(new_game)
            db.session.commit()
        except:
            pass
    
    return redirect(url_for('index'))

@app.route('/clear')
def clear_all():
    db.session.query(Game).delete()
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)