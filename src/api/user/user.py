from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.api.database import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    created_at = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.Date, nullable=True, onupdate=datetime.utcnow)

    # Relacionamento com Role
    role = db.relationship("Role", back_populates="users")
    # Relacionamento com UserClaims
    claims = db.relationship("UserClaim", back_populates="user", lazy="dynamic")

    def __repr__(self):
        return (
            f"<User(id={self.id}, name={self.name}, email={self.email}, "
            f"role_id={self.role_id}, created_at={self.created_at}, updated_at={self.updated_at})>"
        )

class UserClaim(db.Model):
    __tablename__ = "user_claims"

    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), primary_key=True)
    claim_id = db.Column(db.BigInteger, db.ForeignKey("claims.id"), primary_key=True)

    # Relacionamento com User
    user = db.relationship("User", back_populates="claims")
    # Relacionamento com Claim
    claim = db.relationship("Claim", back_populates="user_claims")

    def __repr__(self):
        return f"<UserClaim(user_id={self.user_id}, claim_id={self.claim_id})>"