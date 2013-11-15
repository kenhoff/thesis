#!/usr/bin/env sh
#
# Copyright 2012 Amazon Technologies, Inc.
# 
# Licensed under the Amazon Software License (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
# 
# http://aws.amazon.com/asl
# 
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES
# OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and
# limitations under the License.
 

cd ../..
cd bin
./loadHITs.sh $1 $2 $3 $4 $5 $6 $7 $8 $9 -label ../samples/simple_survey2/simple_survey -input ../samples/simple_survey2/oregon_survey.input -question ../samples/simple_survey2/oregon_survey.xml -properties ../samples/simple_survey2/simple_survey.properties 
./loadHITs.sh $1 $2 $3 $4 $5 $6 $7 $8 $9 -label ../samples/simple_survey2/simple_survey -input ../samples/simple_survey2/numbers_survey.input -question ../samples/simple_survey2/numbers_survey.xml -properties ../samples/simple_survey2/simple_survey.properties 
./loadHITs.sh $1 $2 $3 $4 $5 $6 $7 $8 $9 -label ../samples/simple_survey2/simple_survey -input ../samples/simple_survey2/lightbot_survey.input -question ../samples/simple_survey2/lightbot_survey.xml -properties ../samples/simple_survey2/simple_survey.properties 
./loadHITs.sh $1 $2 $3 $4 $5 $6 $7 $8 $9 -label ../samples/simple_survey2/simple_survey -input ../samples/simple_survey2/darfur_survey.input -question ../samples/simple_survey2/darfur_survey.xml -properties ../samples/simple_survey2/simple_survey.properties 

cd ..
cd samples/simple_survey2
