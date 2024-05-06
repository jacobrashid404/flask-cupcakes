"""Flask app for Cupcakes"""

import os

from flask import Flask, jsonify, request
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
    """Show all cupcakes in database
    Returns JSON {'cupcake':{id, flavor, size, rating, image_url}}
    """

    q_cupcakes = db.select(Cupcake).order_by(Cupcake.id)
    cupcakes = dbx(q_cupcakes).scalars().all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.get("/api/cupcakes/<int:cupcake_id>")
def show_single_cupcake(cupcake_id):
    """Show a single cupcake given its id.
    Returns JSON {'cupcake':{id, flavor, size, rating, image_url}}
    """

    cupcake = db.get_or_404(Cupcake, cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.post("/api/cupcakes")
def create_single_cupcake():
    """Create cupcake from posted JSON data and return it.
    Returns JSON {'cupcake':{id, flavor, size, rating, image_url}}
    """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image_url = request.json["image_url"] or None
    # Right now, if someone is passing in an "", the default won't apply
    # our default will apply if the response evaluates to falsy, so we can set it to None so the DB will use it vs ""

    new_cupcake = Cupcake(
        flavor=flavor,
        size=size,
        rating=rating,
        image_url=image_url
    )

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)
    # option 2: we could return everything in a list, whether single or multiple elements to keep the data structure the same


@app.patch("/api/cupcakes/<int:cupcake_id>")
def update_cupcake(cupcake_id):
    """Update a cupcake using its ID
    Returns JSON {'cupcake':{id, flavor, size, rating, image_url}}
    """

    cupcake = db.get_or_404(Cupcake, cupcake_id)
    cupcake_data = request.json

    # check if each key value has been changed
    # if it's changed, update the cupcake data
    for key in cupcake_data:
        if (key):
            setattr(cupcake, key, cupcake_data[key])

    db.session.commit()
    serialized = cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)


@app.delete("/api/cupcakes/<int:cupcake_id>")
def delete_cupcake(cupcake_id):
    """Deletes a cupcake using its id
    Return JSON {'deleted': cupcake_id}
    """

    cupcake = db.get_or_404(Cupcake, cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return ({"deleted": cupcake_id}, 200)
