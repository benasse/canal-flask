import requests
import concurrent.futures
import datetime
from pytz import timezone
#import pytz
from xml.etree import ElementTree
from werkzeug.contrib.atom import AtomFeed

from flask import request
from flask import Flask
app = Flask(__name__)

url_list_emission='http://service.canal-plus.com/video/rest/getMEAs/cplus/'
url_info_video = 'http://service.canal-plus.com/video/rest/getVideos/cplus/'
tz_paris = timezone('Europe/Paris')

def get_all_video_id(id_emission):
    firstTag = "MEA"
    ids_video = []
    r = requests.get(url_list_emission + id_emission)
    elems = ElementTree.fromstring(r.content)
    for vid in elems.findall( firstTag ):
        id_video = int( vid.findtext( "ID" ) )
        ids_video.append(id_video)
    return ids_video

def add_to_atom(feed_param,ids_video):
    feed = AtomFeed(feed_param['title'], subtitle=feed_param['subtitle'],feed_url=feed_param['url_feed'])
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_to_url = {executor.submit(add_video_feed, id, feed, feed_param): id for id in ids_video}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            if future.exception() is not None:
                print('%r generated an exception: %s' % (url,future.exception()))
    return feed.get_response()

def get_video_info(id_video,feed_param):
    info_video = []
    firstTag = "VIDEO"
    r = requests.get(url_info_video + str(id_video) )
    elems = ElementTree.fromstring(r.content)
    for vid in elems.findall( firstTag ):
        #print ElementTree.tostring( vid )
        description = vid.find( "INFOS" ).findtext("DESCRIPTION")
        publicationTime = vid.find( "INFOS" ).find("PUBLICATION").findtext("HEURE")
        publicationDate = vid.find( "INFOS" ).find("PUBLICATION").findtext("DATE")
        title = vid.find( "INFOS" ).find("TITRAGE").findtext("TITRE")
        subtitle = vid.find( "INFOS" ).find("TITRAGE").findtext("SOUS_TITRE")
        publication_date = datetime.datetime.strptime(publicationDate + publicationTime, '%d/%m/%Y%H:%M:%S')
        publication_date = tz_paris.localize(publication_date)
        info_video= { 'title' : title, 'subtitle' : subtitle , 'publication_date' : publication_date, 'id' : id_video, 'description' : description, 'url' : feed_param['url_lecteur']+ str(id_video)  }
    return info_video

def add_video_feed(id_video,feed,feed_param):
    info_video = get_video_info(id_video,feed_param)
    feed.add(info_video['title'], updated=info_video['publication_date'], id=info_video['id'], url = info_video['url'] )
    return

@app.route('/zapping.atom')
def gen_zapping_feed():
    id_emission = '201'
    feed_param = { 'title' : 'Zapping' , 'subtitle' : 'Le Zapping de Canal+', 'url_feed' : 'http://feed.cicogna.fr/zapping.atom', 'url_lecteur' : 'http://www.canalplus.fr/c-infos-documentaires/pid1830-c-zapping.html?vid=' }

    all_video_id = get_all_video_id(id_emission)
    return add_to_atom(feed_param,all_video_id)

@app.route('/guignols.atom')
def gen_guignols_feed():
    id_emission = '48'
    feed_param = { 'title' : 'Les Guignols' , 'subtitle' : 'Les Guignols de l\'Info', 'url_feed' : 'http://feed.cicogna.fr/guignols.atom', 'url_lecteur' : 'http://www.canalplus.fr/c-divertissement/pid1784-c-les-guignols.html?vid=' }

    all_video_id = get_all_video_id(id_emission)
    return add_to_atom(feed_param,all_video_id)

@app.route('/groland.atom')
def gen_groland_feed():
    id_emission = '254'
    feed_param = { 'title' : 'Groland' , 'subtitle' : 'Made in Groland', 'url_feed' : 'http://feed.cicogna.fr/groland.atom', 'url_lecteur' : 'http://www.canalplus.fr/c-divertissement/pid1787-c-groland.html?vid=' }

    all_video_id = get_all_video_id(id_emission)
    return add_to_atom(feed_param,all_video_id)

@app.route('/lpj.atom')
def gen_lpj_feed():
    id_emission = '249'
    feed_param = { 'title' : 'Le Petit Journal' , 'subtitle' : 'Yann Barthes pesente LE PETIT JOURNAL, un regard decale sur l\'actualite.', 'url_feed' : 'http://feed.cicogna.fr/lpj.atom', 'url_lecteur' : 'http://www.canalplus.fr/c-divertissement/c-le-petit-journal/pid6515-le-petit-journal.html?vid=' }

    all_video_id = get_all_video_id(id_emission)
    return add_to_atom(feed_param,all_video_id)


@app.route('/int-sport-s9.atom')
def gen_int_sport_s9_feed():
    id_emission = '177'
    feed_param = { 'title' : 'Interieur Sport Saison 9' , 'subtitle' : 'Retrouvez tous les docs de la saison 9 d\'Interieur Sport', 'url_feed' : 'http://feed.cicogna.fr/int-sport-s9.atom', 'url_lecteur' : 'http://www.canalplus.fr/c-sport/pid2708-c-interieur-sport.html?vid=' }

    all_video_id = get_all_video_id(id_emission)
    return add_to_atom(feed_param,all_video_id)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
