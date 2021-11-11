from src.app import app
from src.utils import env


if __name__ == '__main__':
    if env('APP_MODE') == 'development':
        app.run(
            host='0.0.0.0',
            port=8000,
            auto_reload=True,
            debug=False,
            access_log=True
        )

    elif env('APP_MODE') == 'production':
        app.run(
            host=env('APP_HOST'),
            port=int(env('APP_PORT')),
            auto_reload=False,
            debug=True if env('APP_DEBUG') == 'true' else False,
            access_log=False
        )
