# Intelligent Model Registry (imr)


[![workflow](https://github.com/eccenca/imr/actions/workflows/check.yml/badge.svg)](https://github.com/eccenca/imr/actions)  


## Quick Start

- Start Artifactory
- Create a repository
- Intelligent Model Registry (imr)
  - repositories (local/remote)
  - publish
  - remove
  - path



### Start Artifactory

```
There are several ways to run Artifactory CE:

Running from a docker image. Just run:

```
$ docker run --name artifactory -d -p 8081:8081 -p 8082:8082 docker.bintray.io/jfrog/artifactory-cpp-ce:latest

```

Download and run from zip file. The Download Page has a link for you to follow. When the file is unzipped, launch Artifactory by double clicking the artifactory.bat(Windows) or artifactory.sh script in the app/bin subfolder, depending on the OS. Artifactory comes with JDK bundled, please read Artifactory requirements.

Once Artifactory has started, navigate to the default URL ```http://localhost:8081```, where the Web UI should be running. The default ```user``` and ```password``` are ```admin:password```.






## Development

- Run [task](https://taskfile.dev/) to see all major development tasks.
- Use [pre-commit](https://pre-commit.com/) to avoid errors before commit.
- This repository was created with [this copier template](https://github.com/eccenca/cmem-plugin-template).