import uvicorn

from app import log_config
from app.factory import create_app

log_config.setup_logging()
app = create_app()

if __name__ == '__main__':
    uvicorn.run("main:app", port=8080, host="0.0.0.0", reload=True, workers=1)
