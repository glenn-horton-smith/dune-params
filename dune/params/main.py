#!/usr/bin/env python
'''
A main command line interface.
'''

import click

@click.group()
def cli():
    pass

@cli.command()
@click.argument('xlsfile', type=click.Path(exists=True))
def dump(xlsfile):
    from . import io
    from jinja2 import Template

    ps = io.load(xlsfile)

    tmpl = Template('''
{% for n,p in params.items() %}{{ p.name}} ({{ n }})\n\t{{ p.value }} {{ p.unit }}
{% endfor %}''')
    s = tmpl.render(params = ps.params)
    click.echo(s)

@cli.command("latex")
@click.option('-t','--template', required=True, type=click.Path(exists=True))
@click.option('-o','--output', required=True, type=click.Path(writable=True))
@click.argument('xlsfile', required=True)
def filter_latex(template, output, xlsfile):
    from . import io, latex
    ps = io.load(xlsfile)
    tmpl = open(template).read()
    text = latex.template(ps, tmpl)
    open(output,'w').write(text)


def main():
    cli(obj={})

if __name__ == '__main__':
    main()
