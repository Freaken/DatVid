#!/bin/sh

if [ `whoami` != root ]; then
	sudo $0
	exit 0
fi

apt-get install texlive-full graphviz dia

TMPDIR=`mktemp -d`
cd $TMPDIR

# fjern eksisterende install
find /usr/local/share/texmf -name '*ku-forside*' | xargs rm -rf
find /usr/local/share/texmf -name '*oberdiek*' | xargs rm -rf

# Download listingsutf8
wget http://mirror.ctan.org/install/macros/latex/contrib/oberdiek.tds.zip
unzip oberdiek.tds.zip -d /usr/local/share/texmf

# Download ku-forside
wget http://www.math.ku.dk/~m00cha/ku-forside.zip
unzip ku-forside.zip -d /usr/local/share/texmf/tex/latex

KUFIL=/usr/local/share/texmf/tex/latex/ku-forside/ku-forside.sty
iconv -f iso-8859-1 -t utf-8 $KUFIL -o ku-forside.sty
mv -f ku-forside.sty $KUFIL

# opdater tex
texhash

# ryd op
cd /
rm -rf $TMPDIR
