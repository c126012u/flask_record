#! /bin/sh

if [ "$*" -eq "10530" ]
then
    export ALSADEV="plughw:2,0"
    k="K2_WAV"

elif [ "$*"  -eq "10500" ]
then
    k="K1_WAV"
fi  

~/julius-kits/dictation-kit-v4.4/bin/linux/julius -C ~/julius-kits/dictation-kit-v4.4/Sample-linux.jconf -record $k -n 10 -output 10 -charconv EUC-JP UTF-8 -module $*

#$./julius_server.sh port
##port はポート番号
##10500 または 10530 を指定する
#export ALSADEV="plughw:1,0"

