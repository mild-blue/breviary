#!/bin/bash
set -e

function build_and_push {
  DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
  echo "Building mildblue/breviary"
  IMAGE_NAME="mildblue/breviary"
  docker build -t "${IMAGE_NAME}" -f "${DIR}/../Dockerfile" "${DIR}/.."
  echo "Pushing ${IMAGE_NAME}."
  docker push "${IMAGE_NAME}"
  echo "Done."
}

function build_and_push_backend {
  build_and_push "backend"
}