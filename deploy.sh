#!/usr/bin/env bash

# adjust version in .env
# adjust version in scripts/.env

start_time="$(date -u +%s)"

cd "$(dirname "$0")"

export $(cat .env)

###############################################################
# Build and push backend
###############################################################
docker-compose -f docker-compose.yml build backend

echo ${DOCKER_PASSWORD} | docker login --username ${DOCKER_USERNAME} --password-stdin

docker tag ${DOCKER_IMAGE_BACKEND}:${VERSION_MTURK_MANAGER} ${DOCKER_USERNAME}/${DOCKER_IMAGE_BACKEND}:${VERSION_MTURK_MANAGER}

docker push ${DOCKER_USERNAME}/${DOCKER_IMAGE_BACKEND}:${VERSION_MTURK_MANAGER}

###############################################################
# Build and push frontend
###############################################################
cd frontend

npm run build
npm run parcel_annotate_build
npm run parcel_sandbox_hit_build
cp sandbox-hit/sandbox-hit.html dist
cp annotate/view.html dist

cd ..

docker-compose -f frontend/docker-compose.yml build frontend

docker tag ${DOCKER_IMAGE_FRONTEND}:${VERSION_MTURK_MANAGER} ${DOCKER_USERNAME}/${DOCKER_IMAGE_FRONTEND}:${VERSION_MTURK_MANAGER}

docker push ${DOCKER_USERNAME}/${DOCKER_IMAGE_FRONTEND}:${VERSION_MTURK_MANAGER}

end_time="$(date -u +%s)"
elapsed="$(($end_time-$start_time))"
echo "Finished in $elapsed seconds"
