# import dictdatabase as DDB

# import logfire

# if True:
#     logfire.configure(send_to_logfire=True, service_name="soiled-py")
# from auth import is_authenticated, not_authorized
from fastapi import FastAPI
from routes import v1_app

app = FastAPI()

# logfire.install_auto_tracing(modules=['src'])
# logfire.instrument_fastapi(app, use_opentelemetry_instrumentation=True)  
# next, instrument your database connector, http library etc. and add the logging handler 

# app.include_router(status.router)
app.mount("/v1", v1_app, name="v1")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)    