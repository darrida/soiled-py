import random
import shelve
from datetime import datetime
from hashlib import sha256

from pydantic import BaseModel, Field


class TestCreds(BaseModel):
    username: str
    hashed_pw: str

    @staticmethod
    def create(username: str, password: str) -> "TestCreds":
        pw_hash = sha256(password.encode("utf-8")).hexdigest()
        user = TestCreds(username=username, hashed_pw=pw_hash)
        with shelve("users.db") as db:
            db[username] = user
        return user

    def update(self, password: str = None):
        with shelve("users.db") as db:
            user: TestCreds = db[self.username]
            if password:
                pw_hash = sha256(password.encode()).hexdigest()
                user.hashed_pw = pw_hash
            db[self.username] = user


class RestAPIUser(BaseModel):
    username: str
    hashed_pw: str = Field(default_factory=sha256(random.random).hexdigest())
    groups: str
    created_by: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_by: str
    updated_at: datetime = Field(default_factory=datetime.now)

    def create(self, password: str):
        pw_hash = sha256(password.encode("utf-8")).hexdigest()
        self.hashed_pw = pw_hash
        with shelve("users.db") as db:
            self.hashed_pw = pw_hash
            self.created_by = "admin"
            self.updated_by = "admin"
            db[self.username] = self

    def update(self, password: str = None):
        with shelve("users.db") as db:
            user: RestAPIUser = db[self.username]
            if password:
                pw_hash = sha256(password.encode()).hexdigest()
                user.hashed_pw = pw_hash
            user.updated_at = datetime.now()
            user.updated_by = "admin"
            db[self.username] = user
    
    @staticmethod
    def get(username: str) -> "RestAPIUser":
        with shelve("users.db") as db:
            user: RestAPIUser = db[username]
        return user
    
    @staticmethod
    def get_all() -> list["RestAPIUser"]:
        with shelve("users.db") as db:
            return db
