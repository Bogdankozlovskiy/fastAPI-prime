from copy import deepcopy


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
tokenUrl = "/users/token/login"
scopes = {
    "me": "Read information about the current user.",
    "items.read": "Read items.",
    "items.write": "Write items."
}
# createuser peewee_user -P
# createdb peewee_db -Opeewee_user
TORTOISE_ORM_DEV = {
    "connections": {"default": "postgres://peewee_user:1234@localhost:5432/peewee_db"},
    "apps": {
        "models": {
            "models": ["modules.users.models", "modules.items.models", "aerich.models"],
            "default_connection": "default"
        }
    }
}
TORTOISE_ORM_TEST = deepcopy(TORTOISE_ORM_DEV)
TORTOISE_ORM_TEST["connections"]["default"] = "sqlite://db.sqlite3"
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]
