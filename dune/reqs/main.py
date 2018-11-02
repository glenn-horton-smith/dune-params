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
    dat = ss.massage(dat);   # fixme: make this an option?

    rendmodname, rendfuncname = render.rsplit('.',1)
    rendmod = importlib.import_module(rendmodname)
    rendfunc = getattr(rendmod, rendfuncname)
    
    text = rendfunc(dat, template)
    open(output,'w').write(text)




@cli.command("getdocdb")
@click.option('--overwrite/--no-overwrite', default=True,
              help='Clobber existing files or not')
@click.option('-t','--tag-file', default="",
              help='If given, write the document id string to given file iff download successful')
@click.option('-e','--extension', default="",
              help='Limit which files to get by matching extension')
@click.option('-a','--archive', default="",
              help='Save files to an archive instead.  If set, give desired extension')
@click.option('-u','--url-pattern',
              default="",
              help='The URL pattern for a DocDB entry')
@click.option('-U','--username', default="dune",
              help="The docdb user name with which to aunthenticate")
@click.option('-P','--password', default="",
              help="The docdb password with which to aunthenticate")
@click.option('-V','--version', default="",
              help="A specific version of the DocDB entry")
@click.argument('docid', required=True)
def getdocdb(overwrite, tag_file, extension, archive, url_pattern, username, password, version, docid):
    '''
    Get contents of a DocDB entry.

    If URL is https:// scheme user/password is required.  http:// is
    assumed to allow anonymous access.
    '''
    url_default_unpw = "https://docs.dunescience.org/cgi-bin/private/ShowDocument?docid={docid}&version={version}"
    url_default_anon = "http://docs.dunescience.org/cgi-bin/ShowDocument?docid={docid}&version={version}"
    if not url_pattern:
        if username and password:
            url_pattern = url_default_unpw
        else:
            url_pattern = url_default_anon


    url = url_pattern.format(**locals())
    #print (url)

    import os
    import sys
    import requests
    import bs4
    from urllib.parse import urlparse, parse_qs

    if url.startswith("http://"): # anon
        res = requests.get(url);
        if not res or not res.ok:
            click.echo("Failed to access anonymous URL %s" % url, err=True)
            sys.exit(-1)
    else:
        from requests.auth import HTTPBasicAuth
        res = requests.get(url, auth=HTTPBasicAuth(username, password))
        if not res or not res.ok:
            click.echo("Failed to access authenticated URL %s" % url, err=True)
            sys.exit(-1)

    #open("foo.html","w").write(res.text);

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    soup_files = soup.find(id='Files')
    if not soup_files:
        click.echo("Failed to access files for docid %s" % docid, err=True)
        sys.exit(-1)

    fileurls = [x.a["href"] for x in soup_files.findAll('li')]
    if not fileurls:
        click.echo("Found no files in docid %s" % docid, err = True)
        sys.exit(-1)

    ident = soup.find(id='BasicDocInfo').findAll('dd')[0].contents[0]
    #print ('found DocDB ident "%s"' % ident)

    # FIXME: should break this state garbage into separate objects and
    # put out to a module.
    if archive:
        afile = ident + '.' + archive
        if not overwrite and os.path.exists(afile):
            sys.exit(-1)

        if 'tar' in archive:
            topts = ['w']
            if 'gz' in archive:
                topts.append('gz')
            topts = ':'.join(topts)
            
            import io, tarfile
            tf = tarfile.open(afile, topts)
            #print ("writing %s" % afile)
            click.echo(afile)
            def save_to_tar(fname, content):
                #print ("\tadding: %s" % fname)
                info = tarfile.TarInfo(fname)
                info.size = len(content)
                tf.addfile(info, io.BytesIO(content))
            saveit = save_to_tar
        else:
            saveit = None
    else:
        def save_as_file(fname, content):
            #print ("saving %s" % fname)
            click.echo(fname)
            with open(fname, 'wb') as fp:
                fp.write(content)
        saveit = save_as_file
            

    for fileurl in fileurls:
        filename = parse_qs(urlparse(fileurl).query)['filename']
        if len(filename) < 1:
            click.echo("failed to find filename in %s" % fileurl)
            continue
        filename = filename[0]

        if extension and not filename.endswith(extension):
            #click.echo("skipping file %s" % filename)
            continue

        if not overwrite and os.path.exists(filename):
            sys.exit(-1)

        if fileurl.startswith("http://"):
            res = requests.get(fileurl)
        else:
            res = requests.get(fileurl, auth=HTTPBasicAuth(username, password))

        saveit(filename, res.content)
    

    if tag_file:
        with open(tag_file, 'w') as fp:
            fp.write(ident);
        

def main():
    cli(obj={})

if __name__ == '__main__':
    main()

