#!/usr/bin/env bash

cd "$(dirname "$0")"

cd frontend

npm run build
npm run parcel_annotate_build
npm run parcel_sandbox_hit_build

cp annotate/view.html dist/
cp sandbox-hit/sandbox-hit.html dist/

cd ..

./start_frontend.sh
