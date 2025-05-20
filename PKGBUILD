# Maintainer: Janis Hutz <development@janishutz.com>
pkgname=biogascontrollerapp
pkgver=3.0
pkgrel=1
pkgdesc="Utility Software to control the Biogas plant of ENATECH at KSWO"
arch=('x86_64')
url="https://github.com/janishutz/BiogasControllerApp"
license=('GPL-3.0-or-later')
depends=('python')
makedepends=('pyinstaller' 'python-setuptools')
source=("biogascontrollerapp/biogascontrollerapp.py")
sha256sums=('SKIP')  # Replace with actual checksum for production use

build() {
  cd "$srcdir"
  pyinstaller --onefile biogascontrollerapp.py
}

package() {
  install -Dm755 "$srcdir/dist/myscript" "$pkgdir/usr/bin/myscript"
}
