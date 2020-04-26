from flask import Flask
from flask import render_template,redirect,url_for
from flask import request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/nist778/nist778/songs/maravilla.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(80), unique=False, nullable=False)
    title = db.Column(db.String(120), unique=False, nullable=False)
    lyrics = db.Column(db.String(800), unique=False, nullable=False)

    def __repr__(self):
        return '%s' % {'title':self.title,'artist':self.artist,'lyrics':self.lyrics}

@app.errorhandler(404)
def page_not_found(e):
    return render_template("doc.html"), 404

@app.route('/')
@app.route('/index')
def index():
    songs = Song.query.all()
    '''
    for song in songs:
        song['title']
        song['artist']
        song['lyrics']
    '''

    return render_template('index.html', song_info=songs )

@app.route('/producto/<name>')
def producto(name):
    return "El producto es " + str(name)

@app.route('/sale/<transaction_id>')
def get_sale(transaction_id):
    return "La transacción es " + str(transaction_id)

@app.route('/dashboard/<msg>')
def dashboard(msg):
    return '%s' % msg

@app.route('/addsong', methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        newsong = Song(
            title=request.form['title'],
            artist=request.form['artist'],
            lyrics=request.form['lyrics']
        )

        db.session.add(newsong)
        db.session.commit()
        return redirect(url_for('dashboard',msg='Success'))
    else:
        return render_template('add_song.html')

'''
TODO: /search/ debería retornar solamente JSON.
Entonces desde la otra página manda consultas AJAX a esta
le devolvemos un JSON y presentamos la información
en el otro lado
'''

@app.route('/search/', methods=['POST','GET'])
def search():
    if request.method == 'POST':
        song_title = request.form['search_string'];
        result = []

        for song in Song.query.filter(Song.title.like(f'{song_title}%')):
            result += [{'artist':song.artist,'title':song.title,'lyrics':song.lyrics}]

        if result == []:
            return render_template('add_song.html',title=song_title,msg='Not found')
        return render_template('songs.html',search_result=result)


if __name__ == '__main__':
    app.run(debug=True,port=8080)
