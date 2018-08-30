#!/bin/bash

mkdir -p ./data_output

# command="docker run -t --restart unless-stopped --mount type=bind,source=$(readlink -f -- data_output),target=/data -p 8005:80 mturk-manager-global-db"
command="docker run -t -d -i --restart unless-stopped --mount type=bind,source=$(readlink -f -- data_output),target=/data -p 8005:80 kritten/mturk-manager-global-db"
is_in_docker_group=$(groups | sed 's/ /\n/g' | grep '^docker$' | wc -l)

if [ $is_in_docker_group -eq 0 ];then
sudo $command
else
$command
fi
exit 0

for config_file; do
  source "$config_file"

  if [ \( -z "$file_settings" \) -o \( -z "$data_output" \) -o \( -z "$port" \) ];then
    echo "USAGE"
    echo "  $0 [OPTIONS] --settings-file <file> --output <directory> --port <port> [--data <directory>]"
    echo "WHERE"
    echo "  --settings-file <file>"
    echo "    Absolute path to the settings file of the corpus"
    echo "  --output <directory>"
    echo "    Absolute path to the output directory of the corpus viewer"
    echo "    output are written"
    echo "  --port <port>"
    echo "    Port under which the container should be accessible"
    echo "  --data <directory>"
    echo "  Absolute path to the directory of the corpus"
    echo "  Only needed if the corpus is not loaded yet"
    exit 1
  fi

  file_settings=$(readlink -f -- $file_settings)
  data_output=$(readlink -f -- $data_output)
  data_corpus=$(readlink -f -- $data_corpus)

  mkdir -p $data_output

  is_in_docker_group=$(groups | sed 's/ /\n/g' | grep '^docker$' | wc -l)

  string_mount_data_output="--volume $data_output:/data"
  string_mount_data_corpus="--volume $data_corpus:/data_corpus:ro"
  string_mount_file_settings="--volume $file_settings:/settings.py:ro"
  string_port="-p $port:80"

  if ! [ -z "$name_container" ];then
    string_name_container="--name $name_container"
  fi

  command="docker run -t -d -i --restart unless-stopped $string_name_container $string_mount_data_output $string_mount_data_corpus $string_mount_file_settings $string_port corpus-viewer"

  if [ $is_in_docker_group -eq 0 ];then
    sudo $command
  else
    $command
  fi
  
done

exit 0