#!/bin/sh

##################
# Infrastructure #
##################

cat orig/cluster.yaml

cp orig/cluster.yaml team-a-infra/.

git add .

git commit -m "Team A infra"

git push