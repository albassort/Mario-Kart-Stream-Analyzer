if [[ ${1} == 'id' ]]; then
    for i in {1..12}; do 
        ls "id/${i}/"|
        while read line; do
            line1=${line##*/}
            line1=${line1%.*}
            line2=${line%%/*}
            jp2a id/${i}/${line} --size=100x40 --chars=01 --html --output=id/${i}html/${line1}.html
            done
        if [[ $(which figlet 2> /dev/null) ]]; then
            figlet '* done *'
        fi
    done    
    echo "1" > cache.txt
elif [[ ${1} == 'convert' ]]; then
    sed -i "${6}s"'/.*/ 0 /' cache.txt
    i=$2
    while [ $i -le "$3" ]; do
    convert ${4}/noprocess${i}.jpg -crop 1500x1500+530+280 -type Grayscale processed/${5}/rank/rank${i}.jpg
    i=$(($i + 1))
    done
    sed -i "${6}s"'/.*/1 /' cache.txt
else
    ls ${2}/*.jpg|
    while read line; do
        line1=${line##*/}
        line1=${line1%.*}
        jp2a ${line} --size=100x40 --chars=01 --html --output=${1}/html/${line1}.html
        done
    if [[ $(which figlet 2> /dev/null) ]]; then
        figlet '* done *'
    fi
    echo "1" > cache.txt
fi
