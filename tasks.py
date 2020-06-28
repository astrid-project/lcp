from __future__ import unicode_literals, absolute_import
from datetime import datetime
from functools import partial
from invoke import task

import os
import sys

ROOT = os.path.dirname(__file__)

CLEAN_PATTERNS = [
    'cover',
    'docs/.build',
    '**/*.pyc',
    '.tox',
    '**/__pycache__',
    'reports',
    '*.egg-info',
]


def color(code):
    '''A simple ANSI color wrapper factory'''
    return lambda t: '\033[{0}{1}\033[0;m'.format(code, t)


green = color('1;32m')
red = color('1;31m')
blue = color('1;30m')
cyan = color('1;36m')
purple = color('1;35m')
white = color('1;39m')


def header(text):
    '''Display an header'''
    print(' '.join((blue('>>'), cyan(text))))
    sys.stdout.flush()


def info(text, *args, **kwargs):
    '''Display informations'''
    text = text.format(*args, **kwargs)
    print(' '.join((purple('>>>'), text)))
    sys.stdout.flush()


def success(text):
    '''Display a success message'''
    print(' '.join((green('>>'), white(text))))
    sys.stdout.flush()


def error(text):
    '''Display an error message'''
    print(red('✘ {0}'.format(text)))
    sys.stdout.flush()


def exit(text=None, code=-1):
    if text:
        error(text)
    sys.exit(-1)


def build_args(*args):
    return ' '.join(a for a in args if a)


@task
def benchmark(ctx, max_time=2, save=False, compare=False, histogram=False, profile=False, tox=False):
    '''Run benchmarks'''
    header(benchmark.__doc__)
    ts = datetime.now()
    kwargs = build_args(
        '--benchmark-max-time={0}'.format(max_time),
        '--benchmark-autosave' if save else None,
        '--benchmark-compare' if compare else None,
        '--benchmark-histogram=histograms/{0:%Y%m%d-%H%M%S}'.format(
            ts) if histogram else None,
        '--benchmark-cprofile=tottime' if profile else None,
    )
    cmd = 'pytest tests/benchmarks {0}'.format(kwargs)
    if tox:
        envs = ctx.run('tox -l', hide=True).stdout.splitlines()
        envs = ','.join(e for e in envs if e != 'doc')
        cmd = 'tox -e {envs} -- {cmd}'.format(envs=envs, cmd=cmd)
    ctx.run(cmd, pty=True)


@task
def clean(ctx):
    '''Clean-up all build artifacts'''
    header(clean.__doc__)
    with ctx.cd(ROOT):
        for pattern in CLEAN_PATTERNS:
            info('Removing {0}', pattern)
            ctx.run('rm -rf {0}'.format(pattern))


@task
def cover(ctx, html=False):
    '''Run tests suite with coverage'''
    header(cover.__doc__)
    extra = '--cov-report html' if html else ''
    with ctx.cd(ROOT):
        ctx.run('pytest --benchmark-skip --cov . --cov-report term {0}'.format(extra),
                pty=True)


@task
def deps(ctx):
    '''Install or update development dependencies'''
    header(deps.__doc__)
    with ctx.cd(ROOT):
        ctx.run("pip3 install -r requirements.txt \
                              -r docs/requirements.txt \
                              -r tests/requirements.txt \
                              -r dev/requirements.txt",
                pty=True)


@task
def pypi(ctx):
    '''Build package for pypi'''
    header(pypi.__doc__)
    with ctx.cd(ROOT):
        ctx.run('python3 setup.py sdist')
        ctx.run('twine upload dist/*')


@task
def docs(ctx):
    '''Build the documentation'''
    header(docs.__doc__)
    with ctx.cd(os.path.join(ROOT, 'docs')):
        ctx.run('make html', pty=True)


@task
def qa(ctx):
    '''Run a quality report'''
    header(qa.__doc__)
    with ctx.cd(ROOT):
        info('Python Static Analysis')
        flake8_results = ctx.run('flake8 . tests',
                                 pty=True, warn=True)
        if flake8_results.failed:
            error('There is some lints to fix')
        else:
            success('No linter errors')
        info('Ensure PyPI can render README and CHANGELOG')
        readme_results = ctx.run(
            'python3 setup.py check -r -s', pty=True, warn=True, hide=True)
        if readme_results.failed:
            print(readme_results.stdout)
            error('README and/or CHANGELOG is not renderable by PyPI')
        else:
            success('README and CHANGELOG are renderable by PyPI')
    if flake8_results.failed or readme_results.failed:
        exit('Quality check failed',
             flake8_results.return_code or readme_results.return_code)
    success('Quality check OK')


def __rst_doc(label):
    def decorator(self):
        self.__doc__ = f'''Convert restructuredText file to {label} using Pandoc'''
        return self

    return decorator


def __rst_convert(caller, ctx, file, format, ext):
    header(caller.__doc__)
    for f in file:
        with ctx.cd(ROOT):
            info(f'rst2{ext}: {f}.rst -> {f}.{ext}')
            ctx.run(
                f'pandoc -s --highlight-style pygments --toc -c pandoc.css -A footer.html -f rst -t {format} {f}.rst -o {f}.{ext}')


@task(iterable=['file'])
@__rst_doc('HTML')
def rst2html(ctx, file):
    __rst_convert(rst2html, ctx, file, format='html', ext='html')


@task(iterable=['file'])
@__rst_doc('Markdown')
def rst2md(ctx, file):
    __rst_convert(rst2md, ctx, file, format='markdown', ext='md')


@task(iterable=['file'])
@__rst_doc('PDF')
def rst2pdf(ctx, file):
    __rst_convert(rst2pdf, ctx, file, format='beamer', ext='pdf')


@task
def tests(ctx, profile=False):
    '''Run tests suite'''
    header(tests.__doc__)
    kwargs = build_args(
        '--benchmark-skip',
        '--profile' if profile else None,
    )
    with ctx.cd(ROOT):
        ctx.run('pytest {0}'.format(kwargs), pty=True)


@task
def tox(ctx):
    '''Run tests against Python versions'''
    header(tox.__doc__)
    ctx.run('tox', pty=True)


RST_FILES = [
    'AUTHORS',
    'CHANGELOG',
    'CONTRIBUTING',
    'README'
]

RST_FILE_ARGS = [f'--file={file}' for file in RST_FILES]


@task(clean, deps, docs, qa,
      partial(rst2md, *RST_FILE_ARGS),
      partial(rst2html, *RST_FILE_ARGS),
      partial(rst2pdf, *RST_FILE_ARGS),
      tests, default=True)
def all(ctx):
    '''Run conversions, tests, reports and packaging'''
    pass
