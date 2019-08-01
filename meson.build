project('imeditor',
        version: '0.8.0',
  meson_version: '>= 0.40.0',
)

i18n = import('i18n')

subdir('data')
subdir('src')

meson.add_install_script('build-aux/meson/postinstall.py')
