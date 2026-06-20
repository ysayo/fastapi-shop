from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    # Локализованные версии (заполняются скриптом автоперевода).
    # Если перевод пуст — используется базовое name/description как фолбэк.
    name_ru = Column(String, nullable=True)
    name_en = Column(String, nullable=True)
    description_ru = Column(Text, nullable=True)
    description_en = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    image_url = Column(String)
    # Дата создания проставляется автоматически:
    #   default       — на стороне приложения (ORM-вставки);
    #   server_default — на стороне БД (любые вставки, новые таблицы).
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        server_default=func.now(),
    )

    category = relationship("Category", back_populates="products")

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"
