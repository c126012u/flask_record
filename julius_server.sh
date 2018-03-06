#! /bin/sh

~/julius-kits/dictation-kit-v4.4/bin/linux/julius -C ~/julius-kits/dictation-kit-v4.4/Sample-linux.jconf -record WAV -n 10 -output 10 -charconv EUC-JP UTF-8 -module $*

#$./julius_server.sh port
##port はポート番号
##10500 または 10530 を指定する
#export ALSADEV="plughw:1,0"
