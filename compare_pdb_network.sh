pdb1=${1}
pdb2=${2}

wd=$(cd $(dirname ${0}); pwd)
mc1=$(mktemp)
mc2=$(mktemp)
graph1=$(mktemp)
graph2=$(mktemp)

#echo ${mc1} ${mc2} ${graph1} ${graph2}

${wd}/MC-Annotate ${pdb1} >${mc1}
${wd}/MC-Annotate ${pdb2} >${mc2}

python ${wd}/parse_mc.py ${mc1} >${graph1}
python ${wd}/parse_mc.py ${mc2} >${graph2}

${wd}/graph_matching ${graph1} ${graph2}

rm ${mc1} ${mc2} ${graph1} ${graph2}

