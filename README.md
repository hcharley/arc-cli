# arc-cli

A command line interface for interacting with the Arc APIs.

## Getting started

**Note: I haven't uploaded to PyPi yet. Please see the [development](#developing)
section to start using right away.**

Install:

```
pip install arc-cli
```

Configure your settings in `~/.arcrc.json`:

```json
{
  "envs": {
    "stage": {
      "url": "https://quickpost-stage.tribdev.com",
      "key": "ABC"
    },
    "local": {
      "url": "http://localhost:8000",
      "key": "ZYX"
    }
  }
}
```

Run a command like so:

```
arc lookup
```

## Commands

More to come soon!

### moveblog

If you need to shuffle a blog from one environment to another, you can use
this command:

```
quickpost moveblog LIVEBLOG_ID FROM_ENV TO_ENV
```

For example, if I want to take blog 703 from stage and move it to
a local development environment run this command (make sure the `stage` and
`local` environments are configured in `~/.quickpost.json`):

```
quickpost moveblog 703 stage local
```

Turn on debugging:

```
quickpost moveblog 703 stage local --debug
```

## Developing

CD into wherever you keep code:

```
cd ~/code/
```

Start a virtualenv:

```
mkvirtualenv quickpost-cli
cd quickpost-cli
```

or

```
virtualenv quickpost-cli
cd quickpost-cli
. bin/activate
cd repo/
```


Clone the repo:

```
git clone git@diggit.trbprodcloud.com:quickpost/quickpost-cli.git .
```

Install requirements:

```
pip install -r requirements.txt
```

Install to your terminal:

```
pip install --editable .
```

That's it. Start using!
