import dataclasses
import typing

from pydantic import BaseModel, Field, create_model


def dataclass_to_basemodel(dc: type) -> type[BaseModel]:
    """Creates a Pydantic BaseModel class from a dataclass, preserving types and defaults."""
    type_hints = typing.get_type_hints(dc)
    fields = {}

    for f in dataclasses.fields(dc):
        annotation = type_hints[f.name]
        if f.default is not dataclasses.MISSING:
            fields[f.name] = (annotation, f.default)
        elif f.default_factory is not dataclasses.MISSING:  # type: ignore[misc]
            fields[f.name] = (annotation, Field(default_factory=f.default_factory))
        else:
            fields[f.name] = (annotation, ...)

    return create_model(dc.__name__, **fields)
