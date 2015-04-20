#!/usr/bin/env python
'''
A main command line interface.
'''

import click

@click.group()
@click.argument('filename')
def cli(ctx, filename):
    ctx.obj['filename'] = filename
    pass

@cli.command()
def dump():
    pass

if __name__ == '__main__':
    cli(obj={})
