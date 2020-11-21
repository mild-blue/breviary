#!/bin/bash
set -e

#GIT_TOKEN="SET_ME"

is_running() {
    service="${1}"
    container_id="$(docker-compose ps -q ${service})"
    health_status="$(docker inspect -f "{{.State.Status}}" "${container_id}")"

    if [ "${health_status}" = "running" ]; then
        echo "${service} status is ${health_status}."
        return 0
    else
        echo "${service} status is ${health_status}."
        return 1
    fi
}

function redeploy {
  echo "Redeploying services."

#  export VERSION_TAG="${1}"
  export VERSION_TAG="latest"
  BACKEND_IMAGE="mildblue/breviary:${VERSION_TAG}"

  # free some nice space
  echo "Removing unused Docker images"
  docker image prune -af

  echo "Pull ${BACKEND_IMAGE} image."
  docker pull "${BACKEND_IMAGE}"

  echo "Stop services."
  docker-compose -f docker-compose.yml stop backend || true
  docker-compose rm -f backend || true

  echo "Deploying new version ${VERSION_TAG}."
  docker-compose -f docker-compose.yml up -d backend

  echo "Checking pod status and waiting until ready."
  while ! is_running "backend"; do sleep 1; done

  echo "Services are ready."
  docker ps
}

VERSION_TAG="latest"
redeploy "${VERSION_TAG}"