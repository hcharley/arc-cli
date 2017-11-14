import os
import json
import click
from ruamel.yaml import YAML



def get_env(env_name):
    """
    Takes a `name`, like `local` and returns an obj like:
        { 'url': 'http://localhost:8000', 'key': 'XXX' }
    """
    config = get_config()

    # Retrieve the environment
    try:
        return config['envs'][env_name]
    except KeyError:
        raise click.UsageError('`{}` environment does not exist'.format(env_name))


def get_config():
    try:
        # Try using a JSON file
        try:
            try:
                with click.open_file(os.path.expanduser("~/.arcrc.json"), 'r') as c:
                    config = json.loads(c.read())
                    validate_config(config)
                    return config
            except ValueError as e:
                click.echo(click.UsageError('~/.arcrc.json file not valid JSON.'))
                raise e
        # Try using a YAML file with .yml extension
        except IOError:
            with click.open_file(os.path.expanduser("~/.arcrc.yml"), 'r') as c:
                yaml=YAML(typ='safe')
                config = yaml.load(c.read())
                validate_config(config)
                return config
        # Try using a YAML file without .yml extension
        except IOError:
            with click.open_file(os.path.expanduser("~/.arcrc"), 'r') as c:
                yaml=YAML(typ='safe')
                config = yaml.load(c.read())
                validate_config(config)
                return config
    # Try using a YAML file
    except IOError:
        click.echo('No configuration found. Please create ~/.quickpost.json')
        raise click.UsageError('No configuration found.')

def validate_config(config):
    if not 'envs' in config:
        raise click.UsageError('Missing envs from config')
    for env_name, env_obj in config['envs'].iteritems():
        if 'url' not in env_obj:
            raise click.UsageError('Missing `url` from {}'.format(env_name))
        if 'key' not in env_obj:
            raise click.UsageError('Missing API `key` from {}'.format(env_name))
    return True


def request_to_curl(request):
    """
    Returns a mimic of a request object as a curl. Useful for debugging.
    curl commands are the CS team's preferred bug reporting method.
    """
    command = "curl -v -X{method} -H {headers} -d '{data}' '{uri}'"

    # Redact the authorization token so it doesn't end up in the logs
    if "Authorization" in request.headers:
        request.headers["Authorization"] = "REDACTED"

    # Format the headers
    headers = ['"{0}: {1}"'.format(k, v) for k, v in request.headers.items()]
    headers = " -H ".join(headers)

    # Return the formatted curl command.
    return command.format(
        method=request.method,
        headers=headers,
        data=request.body,
        uri=request.url
    )
