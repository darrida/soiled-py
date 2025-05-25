from typing import Any


class MaskedStr:
    def __init__(self, secret_value: str) -> None:
        self._secret_value = secret_value

    # Chose this method name because it's what pydantic uses for SecretStr
    def get_secret_value(self) -> str:
        """Get the secret value.

        Returns:
            The secret value.
        """
        return self._secret_value

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and self.get_secret_value() == other.get_secret_value()

    def __hash__(self) -> int:
        return hash(self.get_secret_value())

    def __str__(self) -> str:
        return str(self._display())

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._display()!r})"

    def _display(self) -> str | bytes:
        return "**********" if self.get_secret_value() else ""

    def __bool__(self) -> bool:
        if self.get_secret_value() is None:
            return False
        return True
