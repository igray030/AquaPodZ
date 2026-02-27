from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Snapshot(Base):
    __tablename__ = "snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    quarter: Mapped[str] = mapped_column(String(16), unique=True, index=True)
    source_file: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    records: Mapped[list[Record]] = relationship("Record", back_populates="snapshot", cascade="all, delete-orphan")


class Record(Base):
    __tablename__ = "records"
    __table_args__ = (
        UniqueConstraint("snapshot_id", "function", "category", "subcategory", name="uq_snapshot_path"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    snapshot_id: Mapped[int] = mapped_column(ForeignKey("snapshots.id", ondelete="CASCADE"), index=True)

    function: Mapped[str] = mapped_column(String(64), index=True)
    category: Mapped[str] = mapped_column(String(128), index=True)
    subcategory: Mapped[str] = mapped_column(String(128), index=True)
    maturity_label: Mapped[str] = mapped_column(String(64))
    maturity_score: Mapped[float] = mapped_column(Float)
    weight: Mapped[float] = mapped_column(Float, default=1.0)

    snapshot: Mapped[Snapshot] = relationship("Snapshot", back_populates="records")


class RollupSnapshot(Base):
    __tablename__ = "rollup_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quarter: Mapped[str] = mapped_column(String(16), index=True)
    level: Mapped[str] = mapped_column(String(32), index=True)
    function: Mapped[str | None] = mapped_column(String(64), nullable=True)
    category: Mapped[str | None] = mapped_column(String(128), nullable=True)
    subcategory: Mapped[str | None] = mapped_column(String(128), nullable=True)
    score: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
