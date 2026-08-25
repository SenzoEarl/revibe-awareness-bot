"""PostgreSQL persistence layer.

The repository intentionally stores provenance alongside content so a published
post can always be traced back to its supporting review/evidence records.
"""
from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from typing import Iterable

from sqlalchemy import DateTime, Float, ForeignKey, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

from revibe_bot.models import Review


class Base(DeclarativeBase):
    pass


class ReviewRow(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String(80), index=True)
    source_url: Mapped[str] = mapped_column(Text)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    text: Mapped[str] = mapped_column(Text)
    rating: Mapped[float | None] = mapped_column(Float)
    external_id: Mapped[str | None] = mapped_column(String(255), index=True)
    company_response: Mapped[str | None] = mapped_column(Text)
    content_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    duplicate_of: Mapped[str | None] = mapped_column(String(64))

    claims: Mapped[list["ClaimRow"]] = relationship(back_populates="review", cascade="all, delete-orphan")


class ClaimRow(Base):
    __tablename__ = "claims"

    id: Mapped[int] = mapped_column(primary_key=True)
    review_id: Mapped[int] = mapped_column(ForeignKey("reviews.id"), index=True)
    statement: Mapped[str] = mapped_column(Text)
    attribution: Mapped[str] = mapped_column(String(40))
    category: Mapped[str] = mapped_column(String(80), index=True)
    confidence: Mapped[float] = mapped_column(Float)
    evidence_status: Mapped[str] = mapped_column(String(80), index=True)

    review: Mapped[ReviewRow] = relationship(back_populates="claims")


class Database:
    def __init__(self, url: str) -> None:
        self.engine = create_engine(url, pool_pre_ping=True)

    def create_schema(self) -> None:
        Base.metadata.create_all(self.engine)

    def add_reviews(self, reviews: Iterable[Review]) -> int:
        inserted = 0
        with Session(self.engine) as session:
            for review in reviews:
                existing = session.scalar(
                    select(ReviewRow).where(ReviewRow.content_hash == review.content_hash)
                )
                if existing:
                    continue
                session.add(ReviewRow(**asdict(review)))
                inserted += 1
            session.commit()
        return inserted

    def get_reviews(self, *, source: str | None = None) -> list[ReviewRow]:
        with Session(self.engine) as session:
            stmt = select(ReviewRow).order_by(ReviewRow.published_at.desc())
            if source:
                stmt = stmt.where(ReviewRow.source == source)
            return list(session.scalars(stmt))
