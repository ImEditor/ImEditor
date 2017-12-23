# Maintainer: Hugo Posnic <hugo.posnic@gmail.com>
# Author: Hugo Posnic <hugo.posnic@gmail.com>
# Author: Nathan Seva <nathan.seva@outlook.fr>
pkgname=imeditor
pkgver=0.5
pkgrel=1
pkgdesc="Simple & versatile image editor."
arch=("any")
url="https://github.com/ImEditor/ImEditor"
license=("GPL")
depends=("python" "gtk3" "python-pillow")
source=("$url/archive/$pkgver.tar.gz")
md5sums=("98db5756c25e2f1981ddce3974a7eee8")

build() {
    cd "$srcdir/ImEditor-$pkgver"

    python setup.py build
}

package() {
    cd "$srcdir/ImEditor-$pkgver"
    python setup.py install --root="${pkgdir}" --optimize=1
}
