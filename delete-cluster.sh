#!/bin/sh

###########################
# Deleting infrastructure #
###########################

rm team-a-infra/cluster.yaml

git add .

git commit -m "Remove the cluster"

git push