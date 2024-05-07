# Intelligent Model Registry (imr)


[![workflow](https://github.com/eccenca/imr/actions/workflows/check.yml/badge.svg)](https://github.com/eccenca/imr/actions)  


## Quick Start

- [Start Artifactory](#start-artifactory)
- [Create a repository](#create-a-repository)
- [Intelligent Model Registry (imr) Ops](#inteligent-model-registry-imr-ops)
  - [install](#install)
  - [list](#list)
  - [push](#push)
  - [pull](#pull)
  - [remove](#remove)
  - [path](#path)
- [Using Config File](#using-config-file)



### Start Artifactory


There are several ways to run Artifactory CE:

Running from a docker image. Just run:

```
$ docker run --name artifactory -d -p 8081:8081 -p 8082:8082 docker.bintray.io/jfrog/artifactory-cpp-ce:latest
```

Download and run from zip file. The Download Page has a link for you to follow. When the file is unzipped, launch Artifactory by double clicking the artifactory.bat(Windows) or artifactory.sh script in the app/bin subfolder, depending on the OS. Artifactory comes with JDK bundled, please read Artifactory requirements.

Once Artifactory has started, navigate to the default URL ```http://localhost:8081```, where the Web UI should be running. The default ```user``` and ```password``` are ```admin:password```.

### Create a Repository



### Inteligent Model Registry (imr) Ops

#### install

```
pip install imr
```

#### list


To list all models available in the local repository, execute the command ```imr local list```:
```
imr local list
```

To list all models available in the remote, execute the command ```imr remote list -h REPO -u USER -p PASSWORD```:
 - ```REPO``` repository url i.e. ```http://localhost:8081```
 - ```USER``` user
 - ```PASSWORD``` password
```
imr remote list -h http://localhost:8081 -u user -p password
```

#### push

To publish the model in a local repository, execute the command ```imr local push DIRECTORY PACKAGE -v VERSION``` given the arguments:
 - ```DIRECTORY``` of the model
 - ```PACKAGE``` used to identify the model, i.e ```org.company.department.project.function.mymodel``` 
 - ```VERSION``` optionally (default latest)
```
imr local push DIRECTORY org.company.department.project.function.mymodel -v v0.0.1
```

To publish the model in a remotely repository, execute the command ```imr remote push -h REPO -u USER -p PASSWORD DIRECTORY PACKAGE -v VERSION```:
 - ```REPO``` repository url i.e. ```http://localhost:8081```
 - ```USER``` user
 - ```PASSWORD``` password
 - ```DIRECTORY``` of the model
 - ```PACKAGE``` used to identify the model i.e ```org.company.department.project.function.mymodel``` 
 - ```VERSION``` optionally (default latest)
```
imr remote push -h http://localhost:8081 -u user -p password DIRECTORY org.company.department.project.function.mymodel -v v0.0.1
```

#### pull

The command pull is reserved only for remote repositories.

To pull the model from a remote repository, execute the command ```imr pull -h REPO -u USER -p PASSWORD PACKAGE -v VERSION```:
 - ```REPO``` repository url i.e. ```http://localhost:8081```
 - ```USER``` user
 - ```PASSWORD``` password
 - ```PACKAGE``` used to identify the model i.e ```org.company.department.project.function.mymodel``` 
 - ```VERSION``` optionally (default latest)
```
imr remote pull -h http://localhost:8081 -u user -p password org.company.department.project.function.mymodel -v v0.0.1
```

#### path

To publish the model in a local repository, execute the command ```imr local path PACKAGE -v VERSION``` given the arguments:
 - ```PACKAGE``` used to identify the model, i.e ```org.company.department.project.function.mymodel``` 
 - ```VERSION``` optionally (default latest)
```
imr local path org.company.department.project.function.mymodel -v v0.0.1
```

To publish the model in a remotely repository execute the command ```imr remote path -h REPO -u USER -p PASSWORD PACKAGE -v VERSION```:
 - ```REPO``` repository url i.e. ```http://localhost:8081```
 - ```USER``` user
 - ```PASSWORD``` password
 - ```PACKAGE``` used to identify the model i.e ```org.company.department.project.function.mymodel``` 
 - ```VERSION``` optionally (default latest)
```
imr remote path -h http://localhost:8081 -u user -p password org.company.department.project.function.mymodel -v v0.0.1
```


#### remove

To publish the model in a local repository, execute the command ```imr local rm PACKAGE -v VERSION``` given the arguments:
 - ```PACKAGE``` used to identify the model i.e ```org.company.department.project.function.mymodel``` 
 - ```VERSION``` optionally (default latest)
```
imr local rm org.company.department.project.function.mymodel -v v0.0.1
```

To publish the model in a remotely repository execute the command ```imr remote push -h REPO -u USER -p PASSWORD DIRECTORY PACKAGE -v VERSION```:
 - ```REPO``` repository url i.e. ```http://localhost:8081```
 - ```USER``` user
 - ```PASSWORD``` password
 - ```PACKAGE``` used to identify the model i.e ```org.company.department.project.function.mymodel``` 
 - ```VERSION``` optionally (default latest)
```
imr remote rm -h http://localhost:8081 -u user -p password org.company.department.project.function.mymodel -v v0.0.1
```

### Using config file
Create a config file in your home directory ```~/.imr/imr.conf``` with the following configuration:

```
[mylocalrepo]
type=local
path=~/.imr

[myremoterepo]
type=remote
user=user
password=password
host=http://localhost:8081
```

* Notice that you can have as many repositories as you want.

Now, you can execute your client using the config name i.e ```myremoterepo``` as following:

```
imr remote -c myremoterepo list
```

## Development

- Run [task](https://taskfile.dev/) to see all major development tasks.
- Use [pre-commit](https://pre-commit.com/) to avoid errors before commit.
- This repository was created with [this copier template](https://github.com/eccenca/cmem-plugin-template).
