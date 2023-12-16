#!/bin/bash


echo "Building statics"
cd ui || exit
cat build/index.html || npm run build
cat build/index.html || npm run build

cd ..
echo "Starting api"
source .venv/bin/activate
uvicorn api.app.main:app
