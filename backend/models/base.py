from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    def to_dict(self) -> dict:
        """Safely serialize model column values to a dictionary without relationship recursion."""
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
