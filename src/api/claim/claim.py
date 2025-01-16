from flask_sqlalchemy import SQLAlchemy
from src.api.database import db

class Claim(db.Model):
    __tablename__ = "claims"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    description = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)

    # Relacionamento com UserClaims
    user_claims = db.relationship("UserClaim", back_populates="claim", lazy="dynamic")

    def __repr__(self):
        return f"<Claim(id={self.id}, description={self.description}, active={self.active})>"
