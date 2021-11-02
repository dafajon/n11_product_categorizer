import click
import uvicorn

from .inference_server import make_restful_api

@click.group(help="N11 Product Categorizer Commandline")
def cli():
    pass


@cli.command(help="Serve a trained and dumped model")
@click.option("-m", "--model", help="Name of the model to be served")
@click.option( "-h", "--host", help="Hostname", default="0.0.0.0")
@click.option("-l","--log-level",
              type=click.Choice(['debug', 'info'], case_sensitive=False), help="Logging Level", default="info")
@click.option("-r", "--re_load", is_flag=True, default=False, help="enable/disable auto reload for development.")
@click.option("-p", "--port", help="Port", default=8000)
def serve(model, host, log_level, re_load, port):
    app = make_restful_api(model)
    uvicorn.run(app, host=host, log_level=log_level, reload=re_load, port=port)


if __name__ == '__main__':
    cli()
