# Main Challenges — Week 2 Backend Self-Study

- **Adapting from Node to Python patterns.** Coming from Express/NestJS, I had to adjust to Python project layout and idioms rather than the Node module style I'm used to.
- **FastAPI vs uvicorn split.** `python main.py` didn't start a server — FastAPI only defines the app, and uvicorn is what actually serves it (`uvicorn main:app`). This tripped me up until it clicked.
- **Schema-driven validation.** Getting used to declaring validation on Pydantic schemas instead of writing manual checks like I would in Express.
- **PostgreSQL + environment config.** Wiring the database connection through a `.env` file with `DATABASE_URL`, and using parameterized queries correctly with psycopg.
- **(add your own as they come up)** ______________________________________________