# Backend Task - Clean Architecture

This project is a very naive implementation of a simple shop system. It mimics in its structure a real world example of a service that was prepared for being split into microservices and uses the current Helu backend tech stack.

## Goals

Please answer the following questions:

1. Why can we not easily split this project into two microservices?
2. Why does this project not adhere to the clean architecture even though we have seperate modules for api, repositories, usecases and the model?
3. What would be your plan to refactor the project to stick to the clean architecture?
4. How can you make dependencies between modules more explicit?

### Answers

1. **Why can we not easily split this project into two microservices?**

   There is strong coupling between user/cart and item/inventory:
   - Both modules share the same database/session setup (`be_task_ca/database.py`).
   - `CartItem` in `user/model.py` has a direct foreign key to `items.id`.
   - `user/usecases.py` directly imports item internals (`..item.model.Item`, `..item.repository.find_item_by_id`).
   - Cross-domain communication is done through in-process function calls, not explicit service contracts.

   Because of this, splitting into microservices would still require shared internals or a shared DB schema, which breaks service boundaries.

2. **Why does this project not adhere to clean architecture even though we have separate modules?**

   Dependency direction violates clean architecture principles:
   - Use cases depend on framework/infrastructure details (`fastapi.HTTPException`, `sqlalchemy.orm.Session`).
   - Use cases use transport schemas (`schema.py` / Pydantic) directly instead of application/domain DTOs.
   - Domain models are SQLAlchemy entities (`Base`, ORM mappings), so persistence concerns leak into core logic.
   - Use cases in one module directly depend on repositories/models from another module.

   In clean architecture, inner layers should not depend on frameworks, web, or DB details.

3. **What would be your plan to refactor the project to stick to clean architecture?**

   Proposed incremental plan:
   1. Define explicit bounded contexts (user/cart and item/inventory).
   2. Introduce pure domain/application layers per context (no FastAPI/SQLAlchemy imports).
   3. Define interfaces (`UserRepository`, `ItemRepository`, `LocalInventoryGateway`).
   4. Move SQLAlchemy code to adapters + add mappers (ORM ↔ domain models).
   5. Keep FastAPI in API adapters only (HTTP DTO mapping + exception mapping).
   6. Replace direct cross-module imports with gateway interfaces (later swappable to HTTP/event clients).
   7. Wire dependencies in a composition root (`app.py`) using constructor-based dependency injection.
   8. Add tests by layer: use-case unit tests with in-memory mocks and integration tests for db adapters.

4. **How can you make dependencies between modules more explicit?**

   - Introduce explicit contracts (ABCs / `typing.Protocol`) in a `interface` layer.
   - Use constructor injection instead of importing concrete repositories inside use cases.
   - Keep one composition root that binds interfaces to concrete adapters.
   - Organize code by layers (`domain`, `application`, `adapters/api`, `adapters/db`) with clear direction.
   - Add architecture checks (e.g., import-linter) and enforce them in CI.
   - Use dedicated use-case input/output models to avoid implicit coupling to FastAPI/Pydantic internals.

*Please do not spend more than 2-3 hours on this task.*

Stretch goals:
* Fork the repository and start refactoring
* Write meaningful tests
* Replace the SQL repository with an in-memory implementation

## References
* [Clean Architecture by Uncle Bob](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
* [Clean Architecture in Python](https://www.youtube.com/watch?v=C7MRkqP5NRI)
* [A detailed summary of the Clean Architecture book by Uncle Bob](https://github.com/serodriguez68/clean-architecture)

## How to use this project

If you have not installed poetry you find instructions [here](https://python-poetry.org/).

1. `docker-compose up` - runs a postgres instance for development
2. `poetry install` - install all dependency for the project
3. `poetry run schema` - creates the database schema in the postgres instance
4. `poetry run start` - runs the development server at port 8000
5. `/postman` - contains an postman environment and collections to test the project

## Other commands

* `poetry run graph` - draws a dependency graph for the project
* `poetry run tests` - runs the test suite
* `poetry run lint` - runs flake8 with a few plugins
* `poetry run format` - uses isort and black for autoformating
* `poetry run typing` - uses mypy to typecheck the project

## Specification - A simple shop

* As a customer, I want to be able to create an account so that I can save my personal information.
* As a customer, I want to be able to view detailed product information, such as price, quantity available, and product description, so that I can make an informed purchase decision.
* As a customer, I want to be able to add products to my cart so that I can easily keep track of my intended purchases.
* As an inventory manager, I want to be able to add new products to the system so that they are available for customers to purchase.