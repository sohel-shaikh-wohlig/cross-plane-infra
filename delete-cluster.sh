#!/bin/sh

###########################
# Deleting infrastructure #
###########################

rm team-alfa-infra/cluster.yaml

git add .

git commit -m "Remove infra cluster"

git push