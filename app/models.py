from datetime import datetime
from typing import List
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, Text
from app import db

class User(UserMixin, db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    tickets_created: Mapped[List["Ticket"]] = relationship(
        "Ticket",
        back_populates="author",
        foreign_keys="[Ticket.author_id]"
    )

    tickets_assigned: Mapped[List["Ticket"]] = relationship(
        "Ticket",
        back_populates="assigned_user",
        foreign_keys="[Ticket.assigned_to]"
    )

    comments: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="author"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Ticket(db.Model):
    __tablename__ = "ticket"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default='open')
    priority: Mapped[str] = mapped_column(String(20), default='medium')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    assigned_to: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"), nullable=True)

    author: Mapped["User"] = relationship("User", back_populates="tickets_created", foreign_keys=[author_id])
    assigned_user: Mapped["User"] = relationship("User", back_populates="tickets_assigned", foreign_keys=[assigned_to])
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="ticket", cascade="all, delete-orphan")


class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("ticket.id"), nullable=False)

    author: Mapped["User"] = relationship("User", back_populates="comments")
    ticket: Mapped["Ticket"] = relationship("Ticket", back_populates="comments")
