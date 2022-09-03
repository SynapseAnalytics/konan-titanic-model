#!/bin/bash
if [ $# -eq 0 ]; then
    echo "No arguments supplied"
    echo "Exiting .."
    return 1
fi
if [ -z "$1" ]; then
    echo "Argument is empty"
    echo "Exiting .."
    return 2
fi
if [ "$1" != "knn" ] && [ "$1" != "gaussian" ]; then
    echo "$1 is not a valid model type"
    echo "Model type must be one of: knn, gaussian"
    echo "Exiting .."
    return 3
fi

KONAN_BUILD_PATH="builds/$1"

# Copy over build files
mkdir -p "$KONAN_BUILD_PATH"
cp {Dockerfile,.dockerignore} "$KONAN_BUILD_PATH/"

# Copy over app files
mkdir -p "$KONAN_BUILD_PATH/app"
cp titanic/{retrain.sh,requirements.txt} "$KONAN_BUILD_PATH/app/"
# Copy over app/src files
mkdir -p "$KONAN_BUILD_PATH/app/src"
cp -r titanic/src/app/* "$KONAN_BUILD_PATH/app/src/"
# Copy app/src/utils files
mkdir -p "$KONAN_BUILD_PATH/app/src/utils"
cp -r titanic/src/playground/utils/* "$KONAN_BUILD_PATH/app/src/utils"

# Copy over app/artifacts files
mkdir -p "$KONAN_BUILD_PATH/app/artifacts"
cp data/metadata.yml "$KONAN_BUILD_PATH/app/artifacts/metadata.yml"
export KONAN_MODEL_CLASSIFIER_NAME="$1" && export KONAN_MODEL_ARTIFACTS_PATH="$KONAN_BUILD_PATH/app/artifacts" && python titanic/src/playground/train.py
