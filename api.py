from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import os
import datetime as dt

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'datab.sqlite')
db = SQLAlchemy(app)


songsPostArgs = reqparse.RequestParser()
songsPostArgs.add_argument("name", type=str, help="Name of the song is required", required=True)
songsPostArgs.add_argument("duration", type=int, help="Duration of the song is required", required=True)

songsPutArgs = reqparse.RequestParser()
songsPutArgs.add_argument("name", type=str)
songsPutArgs.add_argument("duration", type=int)

podcastPostArgs = reqparse.RequestParser()
podcastPostArgs.add_argument("name", type=str, help="Name of the podcast is required", required=True)
odcastPostArgs.add_argument("host", type=str, help="Host of the podcast is required", required=True)
podcastPostArgs.add_argument("participants", type=str)
podcastPostArgs.add_argument("duration", type=int, help="Duration of the podcast is required", required=True)

podcastPutArgs = reqparse.RequestParser()
podcastPutArgs.add_argument("name", type=str)
podcastPutArgs.add_argument("host", type=str)
podcastPutArgs.add_argument("participants", type=str)
podcastPutArgs.add_argument("duration", type=int)


audioBookPostArgs = reqparse.RequestParser()
audioBookPostArgs.add_argument("title", type=str, help="Title of the audiobook is required", required=True)
audioBookPostArgs.add_argument("author", type=str, help="Author of the audiobook is required", required=True)
audioBookPostArgs.add_argument("narrator", type=str, help="Narrator of the audiobook is required", required=True)
audioBookPostArgs.add_argument("duration", type=int, help="Duration of the audiobook is required", required=True)

audioBookPutArgs = reqparse.RequestParser()
audioBookPutArgs.add_argument("title", type=str)
audioBookPutArgs.add_argument("author", type=str)
audioBookPutArgs.add_argument("narrator", type=str)
audioBookPutArgs.add_argument("duration", type=int)


songResourceFields = {
    'id': fields.Integer,
    'name': fields.String,
    'duration': fields.Integer,
    'uploadTime': fields.DateTime
}

podcastResourceFields = {
    'id': fields.Integer,
    'name': fields.String,
    'host': fields.String,
    'participants': fields.String,
    'duration': fields.Integer,
    'uploadTime': fields.DateTime
}

audioBookResourceFields = {
    'id': fields.Integer,
    'title': fields.String,
    'author': fields.String,
    'narrator': fields.String,
    'duration': fields.Integer,
    'uploadTime': fields.DateTime
}

class SongModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    duration = db.Column(db.Integer)
    uploadTime = db.Column(db.DateTime,default=dt.datetime.utcnow)


class PodcastModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    duration = db.Column(db.Integer)
    uploadTime = db.Column(db.DateTime,default=dt.datetime.utcnow)
    host = db.Column(db.String(100))
    participants = db.Column(db.Text)


class AudioBookModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    narrator = db.Column(db.String(100))
    duration = db.Column(db.Integer)
    uploadTime = db.Column(db.DateTime,default=dt.datetime.utcnow)


class Songs(Resource):
    @marshal_with(songResourceFields)
    def get(self):
        allSongs = SongModel.query.all()
        return allSongs

class Podcasts(Resource):
    @marshal_with(songResourceFields)
    def get(self):
        allPodcasts = PodcastModel.query.all()
        return allPodcasts

class AudioBooks(Resource):
    @marshal_with(songResourceFields)
    def get(self):
        allAudioBooks = AudioBookModel.query.all()
        return allAudioBooks


class Song(Resource):
    @marshal_with(songResourceFields)
    def get(self, song_id):
        song = SongModel.query.get(song_id)
        if not song:
            abort(404, message="Song doesnt exist.")
        return song

    @marshal_with(songResourceFields)
    def post(self, song_id):
        args = songsPostArgs.parse_args()
        song = SongModel.query.get(song_id)
        if song:
            abort(409, message="Song id already taken select a different id.")
        song = SongModel(id = song_id, name=args['name'], duration=args['duration'])
        db.session.add(song)
        db.session.commit()
        return song, 201

    @marshal_with(songResourceFields)
    def put(self, song_id):
        args = songsPutArgs.parse_args()
        song = SongModel.query.get(song_id)
        if not song:
            abort(404, message="Song doesnt exist")
        if args['name']:
            song.name = args['name']
        if args['duration']:
            song.duration = args['duration']
        db.session.commit()
        return song

    def delete(self, song_id):
        song = SongModel.query.get(song_id)
        if not song:
            abort(404, message="Song doesnt exist")
        db.session.delete(song)
        db.session.commit()
        return 'Song Deleted', 204 


class Podcast(Resource):
    @marshal_with(podcastResourceFields)
    def get(self, podcast_id):
        podcast = PodcastModel.query.get(podcast_id)
        return podcast

    @marshal_with(podcastResourceFields)
    def post(self, podcast_id):
        args = podcastPostArgs.parse_args()
        podcast = PodcastModel(id=podcast_id, name=args['name'], duration=args['duration'], host=args['host'], participants=args['participants'])
        db.session.add(podcast)
        db.session.commit()
        return podcast, 201

    @marshal_with(podcastResourceFields)
    def put(self, podcast_id):
        args = PodcastPutArgs.parse_args()
        podcast = PodcastModel.query.get(podcast_id)
        if not podcast:
            abort(404, message="Podcast doesnt exist")
        if args['name']:
            podcast.name = args['name']
        if args['duration']:
            podcast.duration = args['duration']
        if args['host']:
            podcast.host = args['host']
        if args['participants']:
            podcast.participants = args['participants']
        db.session.commit()
        return podcast

    def delete(self, podcast_id):
        podcast = PodcastModel.query.get(podcast_id)
        if not podcast:
            abort(404, message="Podcast doesnt exist")
        db.session.delete(podcast)
        db.session.commit()
        return 'Podcast delted.', 204

class AudioBook(Resource):
    @marshal_with(audioBookResourceFields)
    def get(self, audiobook_id):
        audioBook = AudioBook.query.get(audiobook_id)
        return audioBook

    @marshal_with(audioBookResourceFields)
    def post(self, audiobook_id):
        args = audioBookPostArgs.parse_args()
        audioBook = AudioBookModel(id=audiobook_id,title=args['title'], duration=args['duration'], author=args['author'], narrator=args['narrator'])
        db.session.add(audioBook)
        db.session.commit()
        return audioBook, 201

    @marshal_with(audioBookResourceFields)
    def put(self, audiobook_id):
        args = audioBookPutArgs.parse_args()
        audioBook = AudioBookModel.query.get(audiobook_id)
        if not audioBook:
            abort(404, message="Audiobook doesnt exist")
        if args['title']:
            audioBook.title = args['title']
        if args['duration']:
            audioBook.duration = args['duration']
        if args['author']:
            audioBook.author = args['author']
        if args['narrator']:
            audioBook.narrator = args['narrator']
        db.session.commit()
        return audioBook

    def delete(self, audiobook_id):
        audioBook = AudioBookModel.query.get(audiobook_id)
        if not audioBook:
            abort(404, message="Audiobook doesnt exist")
        db.session.delete(audioBook)
        db.session.commit()
        return 'Audiobook deleted', 204
        





api.add_resource(Song, '/song/<int:song_id>')
api.add_resource(Songs, '/songs')
api.add_resource(Podcast, '/podcast/<int:podcast_id>')
api.add_resource(Podcasts, '/podcasts')
api.add_resource(AudioBook, '/audiobook/<int:audiobook_id>')
api.add_resource(AudioBooks, '/audiobooks')

if __name__ == '__main__':
    app.run(debug=True)
