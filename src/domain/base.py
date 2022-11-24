from infrastructure.database import Base


class AbstractTable(Base):
    """Abstract base class for all the tables"""
    __abstract__ = True

    def as_dict(self):
        return {column: str(getattr(self, column)) for column in self.__table__.c.keys()}
