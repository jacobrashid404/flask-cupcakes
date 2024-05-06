"""Flask app for Cupcakes"""

import os

from flask import Flask, jsonify
from models import db, dbx, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///cupcakes')
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
db.init_app(app)

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"


@app.get("/api/cupcakes")
def show_all_cupcakes():
    """Show all cupcakes in database"""
    
    q_cupcakes = db.select(Cupcake)
    cupcakes = dbx(q_cupcakes).scalars().all()
    serialized = [c.serialize() for c in cupcakes]
    
    return jsonify(cupcakes=serialized)

@app.get("/api/cupcakes/<int:cupcake_id>")
def show_single_cupcake(cupcake_id):
    