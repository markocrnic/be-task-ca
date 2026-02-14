from be_task_ca.item.adapters.db.repository import SqlAlchemyItemRepository
from be_task_ca.item.application.usecases.create_item import CreateItemUseCase
from be_task_ca.item.application.usecases.list_items import ListItemsUseCase
from be_task_ca.item.schema import CreateItemRequest
from be_task_ca.item.usecases import create_item, get_all
from be_task_ca.user.adapters.db.cart_repository import SqlAlchemyCartRepository
from be_task_ca.user.adapters.db.inventory_gateway import SqlAlchemyInventoryGateway
from be_task_ca.user.adapters.db.user_repository import SqlAlchemyUserRepository
from be_task_ca.user.application.usecases.add_item_to_cart import AddItemToCartUseCase
from be_task_ca.user.application.usecases.create_user import CreateUserUseCase
from be_task_ca.user.application.usecases.list_cart_items import ListCartItemsUseCase
from be_task_ca.user.schema import AddToCartRequest, CreateUserRequest
from be_task_ca.user.usecases import add_item_to_cart, create_user, list_items_in_cart


def test_should_create_user_when_payload_is_valid(db_session):
    request = CreateUserRequest(
        first_name="Marko",
        last_name="Crnic",
        email="marko@example.com",
        password="foobar",
        shipping_address="Street 1",
    )

    response = create_user(request, CreateUserUseCase(SqlAlchemyUserRepository(db_session)))

    assert response.email == "marko@example.com"
    assert response.first_name == "Marko"


def test_should_create_and_list_item_when_payload_is_valid(db_session):
    request = CreateItemRequest(
        name="Book",
        description="FooBar",
        price=39.99,
        quantity=10,
    )

    create_response = create_item(
        request,
        CreateItemUseCase(SqlAlchemyItemRepository(db_session)),
    )
    list_response = get_all(ListItemsUseCase(SqlAlchemyItemRepository(db_session)))

    assert create_response.name == "Book"
    assert len(list_response.items) == 1


def test_should_add_item_to_cart_when_user_and_item_exist(db_session):
    created_user = create_user(
        CreateUserRequest(
            first_name="Marko",
            last_name="Crnic",
            email="marko@example.com",
            password="password",
            shipping_address="Test 2",
        ),
        CreateUserUseCase(SqlAlchemyUserRepository(db_session)),
    )
    created_item = create_item(
        CreateItemRequest(
            name="Keyboard",
            description="Mechanical",
            price=99.0,
            quantity=5,
        ),
        CreateItemUseCase(SqlAlchemyItemRepository(db_session)),
    )

    response = add_item_to_cart(
        created_user.id,
        AddToCartRequest(item_id=created_item.id, quantity=2),
        AddItemToCartUseCase(
            user_repository=SqlAlchemyUserRepository(db_session),
            cart_repository=SqlAlchemyCartRepository(db_session),
            inventory_gateway=SqlAlchemyInventoryGateway(db_session),
        ),
    )

    assert len(response.items) == 1
    assert response.items[0].quantity == 2


def test_should_list_cart_items_for_existing_user(db_session):
    created_user = create_user(
        CreateUserRequest(
            first_name="Marko",
            last_name="Crnic",
            email="marko@example.com",
            password="password",
            shipping_address="Test 3",
        ),
        CreateUserUseCase(SqlAlchemyUserRepository(db_session)),
    )
    created_item = create_item(
        CreateItemRequest(
            name="Keyboard",
            description="Mechanical",
            price=99.0,
            quantity=5,
        ),
        CreateItemUseCase(SqlAlchemyItemRepository(db_session)),
    )
    add_item_to_cart(
        created_user.id,
        AddToCartRequest(item_id=created_item.id, quantity=1),
        AddItemToCartUseCase(
            user_repository=SqlAlchemyUserRepository(db_session),
            cart_repository=SqlAlchemyCartRepository(db_session),
            inventory_gateway=SqlAlchemyInventoryGateway(db_session),
        ),
    )

    response = list_items_in_cart(
        created_user.id,
        ListCartItemsUseCase(SqlAlchemyCartRepository(db_session)),
    )

    assert len(response.items) == 1
    assert response.items[0].item_id == created_item.id
