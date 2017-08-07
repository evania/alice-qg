#! /bin/bash
echo 
echo "The story begins on an ordinary land, then something happens when Alice was sitting with her sister outdoors..."
cd "$(dirname "$0")"
echo "The story begins on an ordinary land, then something happens when Alice was sitting with her sister outdoors..." >> qamatcher/resources/qamatcher/history.txt
cd ../../..
for x in `seq 1 1000`
do
	cd "$(dirname "$0")"
	python historysearch.py
	cd qamatcher
	cd classes
	java -cp .:../resources qamatcher.TestQAResponder
	cd ./..
done