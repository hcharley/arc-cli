import click
import commands


@click.group()
def cli():
    """
    Quickpost-CLI.

    Requires a configuration runcom JSON or YML file placed at ~/arcrc.json
    or ~/arcrc.yml.

    It should look something like this:

    \b
    {
        "envs": {
            "local": {
                "key": "LOCAL_API_KEY",
                "url": "https://localhost:8000"
            },
            "stage": {
                "key": "STAGE_API_KEY",
                "url": "https://quickpost-stage.tribdev.com"
            },
        }
    }

    \b
    envs:
        local:
            key: LOCAL_API_KEY
            url: https://localhost:8000
        stage:
            key: LOCAL_API_KEY
            url: https://localhost:8000

    """
    pass


cli.add_command(commands.search)
