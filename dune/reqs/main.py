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
    import xlrd

    ps = io.load(xlsfile)

    tmpl = Template('''
{% for n,p in params|dictsort %}{{n}} ({{p.name}})\n\t{{ p.value }} {{ p.unit }}
{% endfor %}''')
    s = tmpl.render(params = ps.params)
    click.echo(s)

@cli.command("render")
@click.option('-t','--template', required=True, type=click.Path(exists=True),
              help='Set the template file to use to render the parameters')
@click.option('-r','--render', required=False, default='dune.reqs.latex.render',
              help='Set the rendering module.')
@click.option('-o','--output', required=True, type=click.Path(writable=True),
              help='Set the output file to generate')
@click.argument('xlsfile', required=True)
def render(template, render, output, xlsfile):
    '''
    Render the specs using the template with filtering.
    '''
    import importlib
    import xlrd
    from . import ss
    book = xlrd.open_workbook(xlsfile)
    dat = ss.load_book(book) # fixme make this option to merge with dune-params
    
    rendmodname, rendfuncname = render.rsplit('.',1)
    rendmod = importlib.import_module(rendmodname)
    rendfunc = getattr(rendmod, rendfuncname)
    
    text = rendfunc(dat, template)
    open(output,'w').write(text.encode('utf-8'))




def main():
    cli(obj={})

if __name__ == '__main__':
    main()

