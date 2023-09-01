export TEAM_NAME=$1

export CLUSTER_NAME=$(\
    kubectl get clusters \
    --selector crossplane.io/composite=$TEAM_NAME \
    --output jsonpath="{.items[0].metadata.name}")

export KUBECONFIG=$PWD/kubeconfig.yaml

mkdir -p $TEAM_NAME-apps

touch $TEAM_NAME-apps/dummy

cp -R team-app-reqs $TEAM_NAME-app-reqs

aws eks --region us-east-1 \
    update-kubeconfig \
    --name $CLUSTER_NAME

kubectl create namespace production

#Install Argo CD on newly created Cluster
kubectl create namespace argocd
#Set current context namespace to argocd
kubectl config set-context --current --namespace=argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/core-install.yaml

argocd cluster add \
    $(kubectl config current-context) \
    --name $TEAM_NAME

export SERVER_URL=$(kubectl config view \
    --minify \
    --output jsonpath="{.clusters[0].cluster.server}")

cat orig/team-app-reqs.yaml \
    | sed -e "s@server: .*@server: $SERVER_URL@g" \
    | tee production/$TEAM_NAME-app-reqs.yaml

cat orig/team-apps.yaml \
    | sed -e "s@server: .*@server: $SERVER_URL@g" \
    | tee production/$TEAM_NAME-apps.yaml

git add .

git commit -m "Team A apps"

git push