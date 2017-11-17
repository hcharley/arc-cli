# arc-cli

A command line interface for interacting with the Arc APIs.

[Demo video.](https://drive.google.com/file/d/1boj7cuBdljo1jbWRaNLSuC2ZWlGwihXg/view?usp=sharing)

## Getting started

**Note: I haven't uploaded to PyPi yet. Please see the [development](#developing)
section to start using right away.**

Install:

```
pip install arc-cli
```

Configure your settings in `~/.arcrc.yml`:

```yaml
envs:
    prod:
        key: ARC_KEY=
        url: https://api.tronc.arcpublishing.com
    sandbox:
        key: ARC_KEY=
        url: https://api.sandbox.tronc.arcpublishing.com
    stage:
        key: ARC_KEY=
        url: https://api.staging.tronc.arcpublishing.com
```


or as JSON in `~/.arcrc.json`:

```json
{
  "envs": {
    "prod": {
      "url": "https://api.tronc.arcpublishing.com",
      "key": "ARC_KEY="
    },
    "sandbox": {
      "url": "https://api.sandbox.tronc.arcpublishing.com",
      "key": "ARC_KEY="
    },
    "stage": {
      "url": "https://api.staging.tronc.arcpublishing.com",
      "key": "ARC_KEY="
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

### search

By default this will run a search of Arc's staging environment:

```
arc search
```

To search other environments, explicitly say which one like so:

```
arc search sandbox
```

To search using a P2P ID:

```
arc search --p2pid=1234567
```

To search just published revisions:

```
arc search --pubbed
```

To search just unpublished revisions:

```
arc search --unpubbed
```

By turning on debugging, not only do you get more information on what's
being done over the API, but also *you can get CURLs of the requests
being made so you can share with colleagues*:

```
arc search --debug
```

Once you start searching you'll have an interactive CLI that looks like this:

```bash
(arc-cli) web-george:arc-cli charlex$ arc search --p2pid=74234140
Searching stage with parameters:
	p2p_id: 	74234140

  [####################################]  100%

Loaded 2 of total 2 results.

Results 0 to 10 results:
[0] la-me-ln-nancy-reagan-farewell (unpublished revision)
[1] la-me-ln-nancy-reagan-farewell (published revision)

Choose result index (or input n/p for next/prev results): 1

===================
Arc item:

Arc ID:
	BQGSXV2E4ZGLFOF76FEFLHJF4M

Source system:
	Quickpost

Headline:
	Farewell to Nancy Reagan: Public gathers to pay respects

Slug:
	la-me-ln-nancy-reagan-farewell

Bylines:
	No bylines

Revision is published:
	True

-------------------
Actions:

[0] Return to results
[1] View JSON
[2] Output to JSON file
[3] Get URL to story API
[4] Exit

Action?: 3


URL to story API:
https://api.staging.tronc.arcpublishing.com/story/v2/story/BQGSXV2E4ZGLFOF76FEFLHJF4M
```

## Developing

CD into wherever you keep code:

```
cd ~/code/
```

Start a virtualenv:

```
mkvirtualenv arc-cli
cd arc-cli
```

or

```
virtualenv arc-cli
cd arc-cli
. bin/activate
cd repo/
```


Clone the repo:

```
git clone git@diggit.trbprodcloud.com:quickpost/arc-cli.git .
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
