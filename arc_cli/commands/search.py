import json
import time
import click
import pprint
import logging
import requests
import click_log
from random import randint
from slugify import slugify

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

from arc_cli import utils
from arc_cli.api import Arc
from arc_cli.errors import QuickpostNotFound, QuickpostSlugTaken

logger = logging.getLogger('arc-cli')
click_log.basic_config(logger)


@click.command()
@click.argument('env_name', default='stage', type=str)
@click.option('--p2pid', type=str)
@click.option('--pubbed/--unpubbed', default=None)
@click.option('--pretty/--raw', default=True)
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def search(cntx, env_name, p2pid, pubbed, pretty, debug):
    """
    Move a blog from an environment
    """
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARN)

    conn = Arc(env_name=env_name)

    results = { 'count': 0, 'content_elements': [] }
    params = {}

    # P2P ID
    if p2pid:
        params['p2p_id'] =  p2pid

    # Published
    if type(pubbed) == bool:
        params['published'] =  pubbed

    click.clear()

    click.secho('Searching {} with parameters:'.format(env_name), bold=True)
    for key, val in params.iteritems():
        click.echo('\t{}: \t{}'.format(key, val))

    click.echo('')

    with click.progressbar(length=100) as bar:
        results = conn.search(params)
        bar.update(100)

    count = results['count']
    elements = results['content_elements']

    page_length = 10

    click.secho(
        '\nLoaded {} of total {} result{}.'.format(
            len(elements),
            count,
            's' if count > 1 or count == 0 else '',
            page_length
        ),
        bold=True
    )

    def show_page(start=0):
        click.secho(
            '\nResults {} to {} results:'.format(
                start,
                start+page_length
            ),
            bold=True
        )

        i = 0
        for el in elements[start:start+page_length]:
            # Info on the revision
            if el['revision']['published']:
                revision_str = 'published revision'
            else:
                revision_str = 'unpublished revision'

            # Echo the information to the command line
            click.echo(
                '[{i}] {slug} ({rev_str})'.format(
                    i=i,
                    slug=el.get('slug', 'no-slug-provided'),
                    rev_str=revision_str
                )
            )
            i = i + 1

        click.echo('')
        input_val = click.prompt(
            'Choose result index (or input n/p for next/prev results)'
        )

        if input_val == 'n':
            new_start = start + page_length
            if new_start < count:
                show_page(new_start)
            else:
                click.secho(
                    'Cannot go to a page with no results. Returnning to initial page.',
                    fg='red'
                )
                show_page(start)
            return
        elif input_val == 'p':
            new_start = start - page_length
            if new_start < 0:
                click.secho(
                    'Cannot go to a negative page. Returnning to initial page.',
                    fg='red'
                )
                show_page(start)
            else:
                show_page(start-page_length)
            return

        try:
            selected_i = int(input_val)
        except ValueError:
            click.secho('Invalid selection', fg='red')
            show_page(start)
            return

        try:
            selected_el = elements[selected_i]
        except IndexError:
            click.secho('Invalid selection', fg='red')
            show_page(start)
            return

        def show_actions():
            if selected_el.get('credits', {}).get('by'):
                bylines = ', '.join([b.name for b in selected_el['credits']['by']])
            else:
                bylines = 'No bylines'

            click.secho(
                '\n===================\nArc item:',
                bold=True
            )

            click.echo(
                '\n'.join((
                    '\nArc ID:',
                    '\t' + selected_el['_id'],
                    '\nSource system:',
                    '\t' + selected_el['source']['system'],
                    '\nHeadline:',
                    '\t' + selected_el['headlines']['basic'],
                    '\nSlug:',
                    '\t' + selected_el['slug'],
                    '\nBylines:',
                    '\t' + bylines,
                    '\nRevision is published:',
                    '\t' + str(el['revision']['published']),
                ))
            )

            click.secho(
                '\n-------------------\nActions:',
                bold=True
            )

            click.echo(
                '\n'.join((
                    '\n'
                    '[0] Return to results',
                    '[1] View JSON',
                    '[2] Output to JSON file',
                    '[3] Get URL to story API',
                    '[4] Exit',
                ))
            )
            action_val = click.prompt('\nAction?')

            try:
                action_i = int(action_val)
            except ValueError:
                click.secho('Invalid selection', fg='red')
                return

            click.echo('\n')

            if action_i == 0:
                click.clear()
                show_page(start)
                return
            elif action_i == 1:
                if pretty:
                    json_str = json.dumps(selected_el, indent=2, sort_keys=True)
                    click.echo_via_pager(highlight(json_str, JsonLexer(), TerminalFormatter()))
                else:
                    click.echo(selected_el)
                show_actions()
                return
            elif action_i == 2:
                filename = 'arc-{}--rev-id-{}.json'.format(
                    selected_el['slug'],
                    selected_el['revision']['revision_id'],
                )
                click.secho(
                    'Outputting to JSON named: {}'.format(
                        click.format_filename(filename)
                    ),
                    bold=True
                )
                with click.open_file(filename, 'w') as f:
                    f.write(json.dumps(selected_el, indent=2, sort_keys=True))
                show_actions()
                return
            elif action_i == 3:
                click.secho('URL to story API:', bold=True)
                click.echo(conn.get_story_detail_url(selected_el['_id']))
                show_actions()
                return
            elif action_i == 4:
                cntx.abort()
                return

        show_actions()

    show_page()
