# Maintainer: Hugo Posnic <hugo.posnic@gmail.com>
# Author: Hugo Posnic <hugo.posnic@gmail.com>'gtk3'
imeditor
pkgname=imeditor
pkgver=0.1
pkgrel=1
pkgdesc="Simple & versatile image editor."
arch=("any")
url="https://github.com/ImEditor/ImEditor"
license=('GPL')
depends=('python-pillow')
source=("git+https://github.com/ImEditor/ImEditor.git")
md5sums=("SKIP")

package() {
    cd ${srcdir}/ImEditor
    install -dm755 ${pkgdir}/usr/share/${pkgname}
    cp -R imeditor/* ${pkgdir}/usr/share/${pkgname}
    install -D -m644 ${pkgname}.desktop ${pkgdir}/usr/share/applications/${pkgname}.desktop
}
