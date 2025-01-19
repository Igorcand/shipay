from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, Date, ForeignKey, DateTime, Table
from src.api.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    # Relacionamento com Role (um para muitos)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    role = relationship("Role", back_populates="users")

    # Relacionamento com Claims (muitos para muitos)
    claims = relationship("Claim", secondary="user_claims", back_populates="users", overlaps="user_claims")

    # Relacionamento com UserClaim (muitos para muitos via user_claims)
    user_claims = relationship(
        "UserClaim", back_populates="user", overlaps="claims"
    )

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"

class UserClaim(Base):
    __tablename__ = "user_claims"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    claim_id = Column(UUID(as_uuid=True), ForeignKey("claims.id"), primary_key=True)

    # Relacionamento com o usuário
    user = relationship("User", back_populates="user_claims", overlaps="claims")

    # Relacionamento com a claim
    claim = relationship("Claim", backref="user_claims", overlaps="users")

    def __repr__(self):
        return f"<UserClaim(user_id={self.user_id}, claim_id={self.claim_id})>"