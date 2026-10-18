from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models.annotation import Annotation
    from models.catalog import Catalog


class Video(Base):
    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    catalog_id: Mapped[int] = mapped_column(
        ForeignKey("catalogs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    duration: Mapped[float] = mapped_column(Float, default=0.0)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Hierarchy: Catalog (1) -> Video (N) -> Annotation (N)
    catalog: Mapped["Catalog"] = relationship("Catalog", back_populates="videos")
    annotations: Mapped[list["Annotation"]] = relationship(
        "Annotation", back_populates="video", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"<Video(id={self.id}, catalog_id={self.catalog_id}, title='{self.title}')>"
        )
