from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import BaseModel
import os
from datetime import datetime
from app.services.horoscope_chart import plot_south_indian_chart

class Horoscope(BaseModel):
    __tablename__ = "horoscopes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    gender = Column(String(1), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    time_of_birth = Column(Time, nullable=False)
    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)
    rashi = Column(String(20), nullable=False)
    nakshatra = Column(String(20), nullable=False)
    lagna = Column(String(20), nullable=False)
    planetary_positions = Column(Text, nullable=False)
    chart_image = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    place = relationship("Place", back_populates="horoscopes")

    def __repr__(self):
        return f"<Horoscope {self.name} ({self.rashi})>"

    def save_chart(self, chart_data):
        chart_folder = os.path.abspath("static/horoscope_charts")
        os.makedirs(chart_folder, exist_ok=True)
        chart_path = os.path.join(chart_folder, f"{self.id}.png")
        with open(chart_path, "wb") as f:
            f.write(chart_data)
        self.chart_image = chart_path

    def generate_and_save_chart(self, planetary_positions, birth_details):
        chart_folder = os.path.abspath("static/horoscope_charts")
        os.makedirs(chart_folder, exist_ok=True)
        chart_filename = f"south_indian_chart_{datetime.now().strftime('%Y%m%d%H%M%S')}_{self.name}.png"
        chart_path = os.path.join(chart_folder, chart_filename)
        plot_south_indian_chart(planetary_positions, filename=chart_path, birth_details=birth_details)
        self.chart_image = chart_path 