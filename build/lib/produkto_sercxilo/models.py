from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class FabItem(Base):
    """FAB item."""

    __tablename__ = 'fab_items'

    id = Column(Integer, primary_key=True)

    title = Column(Text)
    product_url = Column(Text, unique=True)
    file_format = Column(Text)
    file_size = Column(Integer)
    file_dimensions_width = Column(Integer)
    file_dimensions_height = Column(Integer)

    images = relationship('Image', back_populates='fab_item')
    description = Column(Text)


class Image(Base):
    """Images urls."""

    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)

    url = Column(Text)
    alt = Column(Text)
    preview = Column(Boolean, default=False)

    fab_item_id = Column(
        Integer, ForeignKey('fab_items.id')
    )
    fab_item = relationship('FabItem', back_populates='images')
