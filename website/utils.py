import os
from functools import partial
from datadog import initialize, statsd

STATSD_HOST = "statsd-exporter"
STATSD_PORT = "9125"

def setting_statsd():
    statsd_options = {
        "statsd_host": os.getenv("STATSD_HOST", STATSD_HOST),
        "statsd_port": os.getenv("STATSD_PORT", STATSD_PORT)
    }

    initialize(**statsd_options)


class StatsdMiddleware:
    def __init__(self, application, app):
        self.__application = application
        self.__app = app

        # send service info with tags
        statsd.gauge("flask.info", 1, tags=[
            f"app:{self.__app}",
        ])

    def __call__(self, environ, start_response):
        patch_info = {
            "app": self.__app, 
            "method": environ['REQUEST_METHOD'],
            "endpoint": environ['PATH_INFO']
        }

        def _start_response(status, headers, *args, **kwargs):
            # log http status code when each response start
            statsd.increment(
                f"flask.request_status_total",
                tags=[
                    f"app:{kwargs.get('app', '')}",
                    f"method:{kwargs.get('method', '')}",
                    f"endpoint:{kwargs.get('endpoint', '')}",
                    f"status:{status.split()[0]}",
                ]
            )
            return start_response(status, headers, *args)

        # timing each request
        with statsd.timed(
            f"flask.request_duration_seconds",
            tags=[
                f"app:{patch_info.get('app', '')}",
                f"method:{patch_info.get('method', '')}",
                f"endpoint:{patch_info.get('endpoint', '')}",
            ],
            use_ms=True
        ):
            return self.__application(environ, partial(_start_response, **patch_info))