#!/bin/sh

##################
# Infrastructure #
##################

cat orig/cluster.yaml

cp orig/cluster.yaml team-alfa-infra/.

git add .

git commit -m "Team Alfa infra"

git push