from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.api.database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    description = Column(String, nullable=True)

    # Relacionamento reverso com os usuários (um para muitos)
    users = relationship("User", back_populates="role")

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
        }
    
    def __repr__(self):
        return f"<Role(id={self.id}, description={self.description})>"