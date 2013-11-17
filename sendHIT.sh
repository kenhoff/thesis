#!/usr/bin/env sh

QUIZ=("oregon" "darfur" "munchers" "lightbot")
# QUIZ[1]="lightbot"
# QUIZ[2]="munchers"
# QUIZ[3]="darfur"


cd ./aws-mturk-clt-1.3.1/bin/

TURK='../../turk_stuff'
echo $TURK

./loadHITs.sh -input $TURK/basic.input -question $TURK/basic.question -properties $TURK/basic.properties

for quiz in ${QUIZ[@]}
do
	./loadHITs.sh -input $TURK/$quiz.input -question $TURK/$quiz.question -properties $TURK/complex.properties
done