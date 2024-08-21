import click

from app.database import db


@click.command()
def init_db():
	"""Initialize the database."""
	db.drop_all()
	db.create_all()
	db.session.commit()
	click.echo("Initialized the database!")
