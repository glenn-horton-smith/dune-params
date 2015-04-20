#!/bin/bash
testdir=$(dirname $(readlink -f $BASH_SOURCE))
srcdir=$(dirname testdir)
workdir=$(mktemp -d)
echo $workdir

maintex=$workdir/main.tex
cat <<EOF > $maintex
\\documentclass{article}
\\usepackage[detect-all=true,group-digits=true,group-separator={,},group-minimum-digits=4,binary-units=true]{siunitx}
\\include{defs}
\\begin{document}
\\include{body}
\\end{document}
EOF

dune-params latex -t $srcdir/templates/latex/defs.tex.j2 -o $workdir/defs.tex $testdir/test-params.xls || exit 1
dune-params latex -t $srcdir/templates/latex/dump.tex.j2 -o $workdir/body.tex $testdir/test-params.xls || exit 1

pushd $workdir 
pdflatex main.tex || exit 1
popd
echo "Removing $workdir"
rm -rf $workdir
 
