from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
db = SQLAlchemy()

class Meteorological(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    freak: Mapped[str] = mapped_column(String(120), nullable=False)
    cat: Mapped[str] = mapped_column(String(120), nullable=False)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    recommendation_list: Mapped[list["Recommendation"]] = relationship(back_populates="freak")
    
    def serialize(self): 
        return {
            "id": self.id,
            "freak": self.freak,
            "cat":self.cat,
            "title":self.title,
            "recommendation": [tip.serialize() for tip in self.recommendation_list]
        }
        
class Recommendation(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    freak_id: Mapped[int] = mapped_column(ForeignKey("meteorological.id"))
    freak : Mapped["Meteorological"] = relationship(back_populates="recommendation_list")
    recommendation: Mapped[str] = mapped_column(String(700), nullable=False)
    
    def serialize(self):
        return{
            "id": self.id,
            "freak_id" : self.freak_id,
            "recommendation": self.recommendation
        }