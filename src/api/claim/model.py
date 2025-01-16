from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Boolean
from src.api.database import Base

class Claim(Base):
    __tablename__ = "claims"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    description = Column(String, nullable=True)
    active = Column(Boolean, nullable=False, default=False)

    # Relacionamento com os usuários
    #users = db.relationship("User", back_populates="role")#, lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "active": self.active,
        }
    
    def __repr__(self):
        return f"<Claim(id={self.id}, description={self.description})>"