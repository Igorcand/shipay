from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String
from src.api.database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    description = Column(String, nullable=True)

    # Relacionamento com os usuários
    #users = db.relationship("User", back_populates="role")#, lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
        }
    
    def __repr__(self):
        return f"<Role(id={self.id}, description={self.description})>"