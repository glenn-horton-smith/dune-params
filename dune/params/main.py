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
    '''
    Dump the fundamental parameters from the given spreadsheet. 
    '''
    from . import io
    from jinja2 import Template

    ps = io.load(xlsfile)

    tmpl = Template('''
{% for n,p in params|dictsort %}{{n}} ({{p.name}})\n\t{{ p.value }} {{ p.unit }}
{% endfor %}''')
    s = tmpl.render(params = ps.params)
    click.echo(s)

@cli.command("render")
@click.option('-t','--template', required=True, type=click.Path(exists=True),
              help='Set the template file to use to render the parameters')
@click.option('-r','--render', required=False, default='dune.params.latex.render',
              help='Set the rendering module.')
@click.option('-o','--output', required=True, type=click.Path(writable=True),
              help='Set the output file to generate')
@click.option('-m','--module', multiple=True,
              help='Set a filter.module.function to filter the parameters')
@click.argument('xlsfile', required=True)
def render(template, render, output, module, xlsfile):
    '''
    Render the parameters using the template with filtering.
    '''

    import importlib
    from . import io
    ps = io.load(xlsfile)

    for modfuncname in module:
        modname, funcname = modfuncname.rsplit('.',1)
        mod = importlib.import_module(modname)
        func = getattr(mod,funcname)
        ps = func(ps)

    rendmodname, rendfuncname = render.rsplit('.',1)
    rendmod = importlib.import_module(rendmodname)
    rendfunc = getattr(rendmod, rendfuncname)
    
    tmpl = open(template).read()
    text = rendfunc(ps, tmpl)
    open(output,'w').write(text)


def main():
    cli(obj={})

if __name__ == '__main__':
    main()
