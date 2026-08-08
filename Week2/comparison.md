# Backend Comparison — FastAPI (Python) vs Node.js (Express / NestJS)

I built the `/items` API in FastAPI this week. My primary stack is Node.js (Express/NestJS), so this note compares the two from that perspective.

## Side-by-side

| Aspect               | FastAPI (Python)                            | Node.js (Express / NestJS)                                                |
| -------------------- | ------------------------------------------- | ------------------------------------------------------------------------- |
| Routing              | Decorators (`@app.get`, `@app.post`)        | Express: `app.get()`, `app.post()` · Nest: `@Get()`, `@Post()` decorators |
| Validation           | Built-in via Pydantic schemas (declarative) | Express: manual or `express-validator` · Nest: `class-validator` + DTOs   |
| Request parsing      | Automatic from the schema                   | Express: `express.json()` middleware · Nest: automatic with DTOs          |
| Auto docs            | Swagger UI at `/docs` out of the box        | Needs setup (`swagger-jsdoc` in Express, `@nestjs/swagger` in Nest)       |
| Type safety          | Python type hints + Pydantic runtime checks | Plain JS (none) in Express · full TypeScript in Nest                      |
| Async model          | `async`/`await` on an ASGI server (uvicorn) | Event loop, promises/`async`-`await`                                      |
| Structure            | Flexible; you organize it yourself          | Express: flexible · Nest: opinionated (modules, providers, DI)            |
| Boilerplate to start | Very low                                    | Express: low · Nest: higher (more setup, more structure)                  |

## What stood out coming from Node

- **Validation is the biggest difference.** In FastAPI I _declare_ the rules on a Pydantic schema and invalid input is rejected automatically with a clean error. In Express I'd hand-write those checks (or add a library); Nest is closer to FastAPI thanks to `class-validator` DTOs, but still needs more wiring.
- **Free interactive docs.** FastAPI's `/docs` (Swagger) works with zero setup, which made testing endpoints fast. In Node I have to configure Swagger myself.
- **The framework/server split surprised me.** In Express the framework starts the server (`app.listen()`). In FastAPI the app is only _defined_; a separate server (uvicorn) runs it (`uvicorn main:app`). Nest is similar to Express here (it bootstraps its own server).
- **Type safety felt familiar via Nest.** Pydantic's runtime validation + type hints reminded me of TypeScript DTOs in Nest, more than of plain Express.

## When I'd pick each

- **FastAPI** — data-heavy APIs where I want validation, typing, and docs handled with minimal code; quick to stand up.
- **Express** — a tiny, explicit, flexible service where I want full control and little structure.
- **NestJS** — larger applications that benefit from an opinionated structure, dependency injection, and TypeScript across the codebase.
