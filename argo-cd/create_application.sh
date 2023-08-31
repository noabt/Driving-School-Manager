#!/bin/bash

# Argo CD API Server and credentials
ARGOCD_SERVER="argocd-server-service.argocd.svc"
ARGOCD_USERNAME="admin"
ARGOCD_PASSWORD=$(argocd admin initial-password -n argocd)
ARGOCD_NAMESPACE="argocd"

# Path to your application YAML file
APP_YAML_PATH=./argo-cd/application.yaml"

# Set the Argo CD context to your desired namespace
kubectl config set-context --current --namespace=$ARGOCD_NAMESPACE

# Log in to Argo CD
argocd login $ARGOCD_SERVER --username $ARGOCD_USERNAME --password $ARGOCD_PASSWORD --insecure

# Apply the application YAML file using kubectl
kubectl apply -f $APP_YAML_PATH

# Sync the application using Argo CD CLI
argocd app sync app-name
