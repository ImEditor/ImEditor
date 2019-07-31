pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'imeditor')
gnome = import('gnome')

gnome.compile_resources('imeditor',
  'imeditor.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python3 = import('python3')

conf = configuration_data()
conf.set('PYTHON', python3.find_python().path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'imeditor.in',
  output: 'imeditor',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

imeditor_sources = [
  '__init__.py',

  'main.py',

  'editor/draw.py',
  'editor/editor.py',
  'editor/image.py',

  'interface/dialog.py',
  'interface/interface.py',
  'interface/tab.py',
  'interface/tools.py',
  'interface/vars.py',

  'filters/base.py'
]

install_data(imeditor_sources, install_dir: moduledir)
