from flask import Flask, request, jsonify, redirect, url_for, render_template, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.types import TIMESTAMP, VARCHAR, SmallInteger, Text, BINARY, BigInteger, Boolean
from sqlalchemy.dialects.mysql import TINYINT, INTEGER, BOOLEAN, LONGTEXT
from os import getenv
from dotenv import load_dotenv
import pymysql
from time import time, strftime, localtime, strptime, mktime
from datetime import datetime
import json
import requests

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
app.config['UPLOAD_FOLDER'] = getenv("UPLOAD_FOLDER")
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600
app.config['SECRET_KEY'] = getenv("SECRET_KEY")

db = SQLAlchemy(app)

class Farm(db.Model):
   __tablename__ = 'farm'
   id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
   name = db.Column(db.String(10))
   ip = db.Column(db.Integer)
   sol = db.Column(db.Integer)
   power = db.Column(db.Integer)
   cards = db.Column(db.Integer)
   sw = db.Column(db.Float)
   ping  = db.Column(db.Float)
   tlife = db.Column(db.Float)
   tstop = db.Column(db.BigInteger)
   owner = db.Column(db.SmallInteger)
   electricity = db.Column(db.Float)
   acp = db.Column(db.Integer)
   rej = db.Column(db.Integer)
   algo = db.Column(db.Integer)
   port = db.Column(db.Integer)
   miner = db.Column(db.Integer)
   active = db.Column(TINYINT)
   uptime = db.Column(db.BigInteger)
   os = db.Column(db.Integer)
   login = db.Column(db.Integer)
   place = db.Column(TINYINT)
   nvidia_driver = db.Column(db.String(12))
   remote_address = db.Column(db.Integer)

   def __repr__(self):
      return "<{}>".format(self.name)

exch_names = {'remote_address':'remote ip','nvidia_driver':'drv'}

# -------------------------------------------------------------------------------------------  УК
def get_table(tbl):
   recs = db.session.query(tbl).all()
   table=[]
   index=[]
   #bts={}
   res={}
   i=0
   if recs:
      for line in recs:
         i+=1
         row={}
         for field_name in dir(tbl):
            if field_name in exch_names:
               if i == 1:
                  index.append(exch_names[field_name])
               row[exch_names[field_name]] = getattr(line, field_name)
            else:
               if not '__' in field_name and field_name[0] != '_':
                  value = getattr(line, field_name)
                  if type(value) in (int, str):
                     if i == 1:
                        index.append(field_name)
                     row[field_name] = value
         table.append(row.copy())
         #l={}
         #l['edit'] = url_for('edits', tbl=tbl, id=d.id)
         #l['del'] = url_for('deletes',  tbl=tbl, id=d.id)
         #if tbl == 'Ka':
         #   l['price'] = url_for('load_price', id=d.id)
         #l['service'] = url_for('edit'+pref, id=d.id)
         #bts[d.id]=l.copy()
         res['t'] = table
         res['idx'] = index
         #res['bts'] = bts
         #res['new'] = url_for('news',tbl=tbl)
   else:
      res['t'] =False
   #res['new'] = url_for('news', tbl=tbl)
   return res


@app.route('/')
def hello_world():
   return render_template("dashboard.html")

@app.route('/dash/farm/')
def dash_farm():
   d={}
   d = get_table(Farm)
   #d['title'] = get_tbl_title(tbl)
   #d['tbl'] = tbl
   return render_template("dashfarm.html", d=d)


if __name__ == '__main__':
   app.run()
