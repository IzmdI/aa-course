import datetime

from sqlalchemy import BigInteger, Boolean, Column, DateTime, func

from auth.src.db.declarative import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False, index=True, comment="Идентификатор")
    created_at = Column(DateTime, nullable=False, comment="дата и время создания", default=datetime.datetime.now)
    updated_at = Column(
        DateTime,
        nullable=False,
        comment="дата и время последнего обновления",
        default=datetime.datetime.now,
        server_default=func.now(),
        onupdate=func.now(),
    )
    is_active = Column(Boolean, nullable=False, comment="логическое удаление объекта", default=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def as_dict_lower(self):
        return {str.lower(c.name): getattr(self, c.name) for c in self.__table__.columns}
