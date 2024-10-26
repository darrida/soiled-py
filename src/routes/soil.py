import logfire
from fastapi import Response, status
from fastapi.routing import APIRouter
from models.soil import Location

router = APIRouter()


# logfire.configure(pydantic_plugin=logfire.PydanticPlugin(record='all')) 

@router.post("/moisture")
def create_soil_measurement(data: Location):
    logfire.info(f"this is the data: {str(data)}")
    thing = sub_function(data)
    data.description = thing

    logfire.debug(data)
    return data


@router.get("/moisture")
def get_soil_moisture_levels(): ...


@router.get("/moisture/plant/{id}")
def get_plant_moisture_levels(): ...


@router.get("/moisture/plant/{id}/last")
def get_plant_last_soil_moisture_level(): ...





def sub_function(data: Location):
    logfire.info(data.description)
    raise Exception
    new_data = Location(name="new", description="thing", active=True)
    return new_data
