from flask import Flask, redirect, url_for, render_template, json, request, Markup
app = Flask(__name__)

@app.route('/')
def root():	
	with app.open_resource('static/json/artist_details.json') as artists:
		artist_data = json.load(artists)
		total_artists = len(artist_data)
	with app.open_resource('static/json/album_details.json') as albums:
		album_data = json.load(albums)
		total_albums = len(album_data)
	
	tracklist_per_album = []
	tracklist = []
	with app.open_resource('static/json/album_tracks.json') as tracks:
		track_data = json.load(tracks)
		for album in track_data:
			tracklist_per_album.append(album)
			album_tracks = album["tracks"]
			for track in album_tracks:
				tracklist.append(track)
		total_tracks = len(tracklist)
	return render_template('index.html', artistlen=total_artists, artists=artist_data, albumlen=total_albums, albums=album_data, tracklen=total_tracks, tracks=tracklist_per_album)
		

@app.route('/artists/')
def artists():
	with app.open_resource('static/json/artist_details.json') as artists:
		artist_data = json.load(artists)
		
	return render_template('artists.html', artists=artist_data)

@app.route('/albums/')
def albums():
	artist_id_requested = str(request.args.get('artist'))
	artist_name = str(request.args.get('artname'))	
	artists_albums = []
	with app.open_resource('static/json/album_details.json') as albums:
		album_data = json.load(albums)
		for obj in album_data:
			artist_id = str(obj["artist_id"])
			if artist_id == artist_id_requested:
				artists_albums.append(obj)		

	return render_template('albums.html', albums=artists_albums, artname=artist_name)

@app.route('/tracks/')
def tracks():
	album_id_requested = str(request.args.get('album'))
	track_selected = str(request.args.get('playtrack'))

	album_dets = []
	with app.open_resource('static/json/album_details.json') as albums:
		album_data = json.load(albums)
		for obj in album_data:
			album_id = str(obj["album_id"])
			if album_id == album_id_requested:
				album_dets = obj


	tracklist = []
	with app.open_resource('static/json/album_tracks.json') as tracks:
		track_data = json.load(tracks)
		for album in track_data:
			obj_album_id = str(album["album_id"])
			if obj_album_id == album_id_requested:
				tracklist = album["tracks"]

	total_tracks = len(tracklist)

	track_lyrics = "" 
	with app.open_resource('static/json/track_lyrics.json') as lyrics:
		lyric_data = json.load(lyrics)
		for lyric in lyric_data:
			lyric_album_id = str(lyric["album_id"])
			lyric_track_no = str(lyric["track"])
			if lyric_album_id == album_id_requested:
				if lyric_track_no == track_selected:
					these_lyrics = lyric["lyrics"]
					track_lyrics = Markup(these_lyrics)	
	
	if track_selected != "None":
		track_arr_index = int(request.args.get('playtrack'))-1
	else:
		track_arr_index = track_selected
	
	return render_template('tracks.html', album_info=album_dets, tracks=tracklist, lentracks=total_tracks, play=track_arr_index, lyrics=track_lyrics)
	
if __name__ == '__main__':
	app.run(debug=True)
