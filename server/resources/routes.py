from server import app
from flask import request, make_response,jsonify
import requests
import json
from playhouse.shortcuts import model_to_dict

from server.models.models import Album, Photos


@app.route('/')
def hello_world():
    return 'Hello, World'

@app.route('/load/<table_name>', methods=['GET', 'POST'])
def load_table(table_name):
    if request.method == 'GET':
        num_registros = 0
        if table_name == 'album':
            num_registros = Album.select().count()
        elif table_name == 'photos':
            num_registros = Photos.select().count()
    elif request.method == 'POST':
        if table_name == 'album':
            resp = requests.get('https://jsonplaceholder.typicode.com/albums')
            albums_list = json.loads(resp.text)
            records_list = [ {'id': album['id'], 'titulo': album['title']}  for album in albums_list ]
            Album.insert_many(records_list).execute()
            num_registros = Album.select().count()
        if table_name == 'photos':
            resp = requests.get('https://jsonplaceholder.typicode.com/photos')
            photos_list = json.loads(resp.text)
            records_list = [ {'id': photo['id'], 'titulo': photo['title'], 'url': photo['url']}  for photo in photos_list ]
            Photos.insert_many(records_list).execute()
            num_registros = Photos.select().count()

    response = make_response(
        jsonify({
            "total_registros": num_registros
        })
    )
    return response

@app.route('/<table_name>')
def get_records(table_name):
    if table_name == 'albums':
        records = Album.select()
        record_array = []
        for record in records:
            record_dict = {
                "id": record.id,
                "titulo": record.titulo
            }
            record_array.append(record_dict)

    response = make_response(
        jsonify({
            "rows": record_array
        })
    )
    return response

@app.route('/photos/<id_album>')
def get_photos(id_album):
    records = Photos.select(Photos.id, Photos.titulo, Photos.url, Photos.thumb).where(Photos.album_id == id_album).order_by(Photos.album_id)
    records_list = [ model_to_dict(photo)  for photo in records ]
    if len(records_list) == 0:
        resp = requests.get('https://jsonplaceholder.typicode.com/photos?albumId=' + id_album)
        photos_list = json.loads(resp.text)
        records_list = [ {
            'id': photo['id'],
            'titulo': photo['title'],
            'url': photo['url'],
            'thumb': photo['thumbnailUrl'],
            'album_id': photo['albumId']
            }  for photo in photos_list ]
        Photos.insert_many(records_list).execute()
        records = Photos.select(Photos.id, Photos.titulo, Photos.url, Photos.thumb).where(Photos.album_id == id_album).order_by(Photos.album_id)
        records_list = [ model_to_dict(photo)  for photo in records ]

    response = make_response(
        jsonify({
            "photos": records_list
        })
    )

    return response