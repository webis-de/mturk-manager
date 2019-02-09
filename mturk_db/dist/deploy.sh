#./build.sh
sudo docker login -u kritten -p St3ckd0s3!
sudo docker tag mturk-manager-global-db kritten/mturk-manager-global-db:latest
sudo docker push kritten/mturk-manager-global-db:latest