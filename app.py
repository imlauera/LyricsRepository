from flask import Flask
from flask import render_template,redirect,url_for
from flask import request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///maravilla.db'
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
    return "404"

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

@app.route('/output/<msg>')
def output(msg):
    return render_template('output.html',msg=msg)

@app.route('/addsong', methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        if request.form['title'] != '' and request.form['artist'] and request.form['lyrics']:
            return redirect(url_for('output',msg="Failed. The fields can't be empty"))
        newsong = Song(
            title=request.form['title'],
            artist=request.form['artist'],
            lyrics=request.form['lyrics']
        )

        db.session.add(newsong)
        db.session.commit()
        return redirect(url_for('output',msg='Success'))
    else:
        return render_template('add_song.html')

'''
TODO: /search/ debería retornar solamente JSON.
Entonces desde la otra página manda consultas AJAX a esta
le devolvemos un JSON y presentamos la información
en el otro lado
'''

@app.route('/search/', methods=['GET'])
def search():
    if request.method == 'GET':
        song_title = request.args.get('q');
        print(song_title)
        result = []

        for song in Song.query.filter(Song.title.like(f'{song_title}%')):
            result += [{'artist':song.artist,'title':song.title,'lyrics':song.lyrics,'id':song.id}]

        if result == []:
            return render_template('add_song.html',title=song_title,msg='Not found')
        return render_template('songs.html',search_result=result)


@app.route('/editsong',methods=['GET','POST'])
@app.route('/editsong/<song_id>', methods=['POST','GET'])
def edit(song_id=None):
    if request.method == 'GET':
        song = Song.query.filter_by(id=song_id).first()
        if song == None:
          return redirect(url_for('output',msg="ID not found"))
        return render_template('edit_song.html',id=song.id,title=song.title, artist=song.artist, lyrics=song.lyrics)
    elif request.method == 'POST':
        song = Song.query.filter_by(id=request.form['id']).first()
        print(request.form['id'])
        song.title = request.form['title']
        song.artist = request.form['artist']
        song.lyrics = request.form['lyrics']

        db.session.commit()
        return redirect(url_for('output',msg='Success'))

#/deletesong/Metallica/Master of Puppets
@app.route('/deletesong/<artist>/<title>',methods=['GET'])
def delete(artist=None, title=None):
    song = Song.query.filter_by(artist=artist, title=title).delete()
    db.session.commit()
    return redirect(url_for('output',msg='Success'))

    
if __name__ == '__main__':
    app.run(threaded=True,port=8080)
