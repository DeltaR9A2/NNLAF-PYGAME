#!/bin/bash
if [ ! -d ./temp ]; then
	mkdir ./temp
fi

for file in *.ogg; do
	ffmpeg -i $file -vn -ac 2 -c:a libvorbis ./temp/$file; 
done
