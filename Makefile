run:
	@uvicorn workout.main:app --reload


create-migrations:
	@python -m alembic revision --autogenerate -m $(d)

run-migrations:
	@python -m alembic upgrade head