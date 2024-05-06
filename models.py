"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
dbx = db.session.execute


class Cupcake(db.Model):
    """Cupcake model"""

    __tablename__ = "cupcakes"

    id = db.mapped_column(
        db.Integer,
        db.Identity(),
        primary_key=True
    )

    flavor = db.mapped_column(
        db.String(50),
        nullable=False
    )

    size = db.mapped_column(
        db.String(15),
        nullable=False
    )

    rating = db.mapped_column(
        db.Integer,
        nullable=False
    )

    image_url = db.mapped_column(
        db.String(500),
        # FIXME: we want to make this a global var (for urls) for reusaibility and imports
        default="https://tinyurl.com/demo-cupcake",
        nullable=False
    )

    def serialize(self):
        """serialize to dictionary"""

        return {
            "id": self.id,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
            "image_url": self.image_url
        }
