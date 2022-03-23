#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sites import app
from logging.config import dictConfig
import yaml
import click


@click.command()
@click.option('--port', default=8933)
def run(port):
    app.run(host='0.0.0.0', port=port, threaded=True, debug=app.config.get('DEBUG', False))


if __name__ == '__main__':
    dictConfig(yaml.safe_load(open('logconfig.yaml', 'r')))
    run()

