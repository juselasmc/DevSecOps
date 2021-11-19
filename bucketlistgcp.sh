#!/bin/bash
#This code list all buckets in all the projects in GCP
echo "PROJECT, BUCKET"
for project in  $(gcloud projects list --format="value(projectId)")
do
  #echo "ProjectId:  $project"
  gcloud config set project $project --no-user-output-enabled
    for bucket in $(gsutil ls)
        do
            echo "$project, $bucket"
        done
done
