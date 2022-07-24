#!/bin/bash
# create an array
names=(
    # 'res1.xml'
    # 'res2.xml'
    # 'res3.xml'
    # 'res4.xml'
    'res5-1.xml'
    'res5-2.xml'
    'res6-1.xml'
    'res6-2.xml'
    'res7-1.xml'
    'res7-2.xml'
    'res8-1.xml'
    'res8-2.xml'
    'res8-3.xml'
    'res8-4.xml'
)

for name in ${names[@]}; do
wget -O $name.bz2 "https://zenodo.org/record/6720296/files/$name.bz2?download=1"
bzip2 -d $name.bz2
done

# xmlmerge *.xml > ../merged.xml
