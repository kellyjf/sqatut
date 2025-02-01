#!/usr/bin/python3
from argparse import ArgumentParser as ap
import signal


import sqlalchemy
import sqlalchemy.orm

from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy import select

class Base(DeclarativeBase):
	pass

class Book(Base):
	__tablename__ = "books"
	id : Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column(String)
	subject: Mapped[str] = mapped_column(String)
	format: Mapped[str] = mapped_column(String)
	year: Mapped[int]

class Subject(Base):
	__tablename__ = "subjects"
	id : Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column(String)

class Option(Base):
	__tablename__ = "options"
	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str]
	type: Mapped[str]

	__mapper_args__ = {
		"polymorphic_on": "type",
		"polymorphic_identity": "all"
	}

class ColorOption(Option):
	spec: Mapped[Optional[str]]=mapped_column(String(6))
	__mapper_args__ = {
		"polymorphic_identity": "color"
	}

class PartyOption(Option):
	__mapper_args__ = {
		"polymorphic_identity": "party"
	}

if __name__ == "__main__":
	signal.signal(signal.SIGINT,signal.SIG_DFL)
	parser=ap()
	parser.add_argument("--list","-l", action="store_true", help="List Database")
	args=parser.parse_args()

	engine=sqlalchemy.create_engine("sqlite+pysqlite:///test.db", echo=True)

	Book.metadata.create_all(engine)

	session=sqlalchemy.orm.Session(engine)


	session.add(ColorOption(name="Blue"))
	session.add(ColorOption(name="Red"))
	session.add(ColorOption(name="Green", spec="00FF00"))
	session.add(PartyOption(name="Democrat"))
	session.add(PartyOption(name="Republican"))
	session.add(PartyOption(name="Fascist"))
	session.commit()

	stmt=select(ColorOption).order_by(ColorOption.name)
	print(session.scalars(stmt).all())


	res=session.execute(sqlalchemy.text("select date();"))
	for r in res:
		print(r)



