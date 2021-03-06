import flask
import os
import urllib.parse
import redis
from flask import send_from_directory

url = urllib.parse.urlparse(os.environ.get('REDISCLOUD_URL'))
r = redis.Redis(host=url.hostname, port=url.port, password=url.password)

app = flask.Flask(__name__)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/favicon.png')


@app.route('/')
@app.route('/home')
def home():
    r = redis.Redis(
        password='redislabs',
        decode_responses=True,
        host='redis-12000.yonicluster.primary.cs.redislabs.com',
        port=12000,
        ssl=True,
        ssl_keyfile='./client.key',
        ssl_certfile='./client.crt',
        ssl_cert_reqs='required',
        ssl_ca_certs='./proxy_cert.pem',
    )
    info = r.info()
    return info


if __name__ == "__main__":
    app.secret_key = 'ItIsASecret'
    app.debug = True
    app.run()
