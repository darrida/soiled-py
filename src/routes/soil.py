import logfire
from fastapi import Response, status
from fastapi.routing import APIRouter
from models.soil import Location

router = APIRouter()


# logfire.configure(pydantic_plugin=logfire.PydanticPlugin(record='all')) 

@router.post("/")
def get_soil(data: Location):
    logfire.info(f"this is the data: {str(data)}")
    thing = sub_function(data)
    data.description = thing

    logfire.debug(data)
    return data


def sub_function(data: Location):
    logfire.info(data.description)
    raise Exception
    new_data = Location(name="new", description="thing", active=True)
    return new_data
