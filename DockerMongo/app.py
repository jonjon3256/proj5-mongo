import os
from flask import Flask, redirect, url_for, request, render_template
import flask
from pymongo import MongoClient
import arrow
import acp_times
import config
import logging


app = flask.Flask(__name__)
CONFIG = config.configuration()
#app.secret_key = CONFIG.SECRET_KEY

client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
db = client.tododb

datalist = []



@app.route('/')
@app.route('/todo')
def todo():
    _items = db.tododb.find()
    items = [item for item in _items]

    return flask.render_template('todo.html', items=items)

@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("todo")
    return flask.render_template('404.html'), 404


@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))


    b_dist = request.args.get('b_dist',type=int)
    start_d = request.args.get('start_d',type=str)
    start_time = request.args.get('start_time',type=str)
    start = start_d +" "+ start_time
    
   
    # FIXME: These probably aren't the right open and close times
    # and brevets may be longer than 200km
    
    
    open_time = acp_times.open_time(km,b_dist,start)
    close_time = acp_times.close_time(km,b_dist,start)
    result = {"open": open_time, "close": close_time}
    data_list = {"open":open_time, "close": close_time}
    datalist.append(data_list)
    return flask.jsonify(result=result)

@app.route('/_new', methods=['POST'])
def _new():
    for item_doc in datalist:
        db.tododb.insert_one(item_doc)
    while (datalist != []):
        datalist.pop()

    return redirect(url_for('todo'))


@app.route("/_display",methods=['POST'])
def _display():
    _items = db.tododb.find()
    items = [item for item in _items]

    return render_template('display.html', items=items)

    

#############

#app.debug = CONFIG.DEBUG
#if app.debug:
#    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug =True)
