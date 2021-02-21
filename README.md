This is still a WIP

# Context
* Given a directory containing all dependencies of a Java project
* I want to deploy all of them into an specific self-hosted Apache Maven Repository
* Deploy-file goal from [Apache Maven Deploy plugin](https://maven.apache.org/plugins/maven-deploy-plugin/deploy-file-mojo.html), allows me to upload a single file into a remote repository.
    * Deploying all files one by one over the command line is a never ending task.
* With a Maven multi module project. Each module deploying a single file into the remote repository. All pom.xml of this modules, will be the same but for specific path and jar file
    * [Jinja 2](https://jinja.palletsprojects.com/en/2.11.x/) templating engine

This repository is a PoC of automatically building that Apache Maven multi-module project which will enable us to upload lots of files to a remote repository

# Related gists
* [Download all maven dependencies into a folder using maven docker image](https://gist.github.com/misTrasteos/36ef4edd8443acb826bf100b416ca79e)
* [Self hosted Apache Maven repository, Reposilite, PoC](https://gist.github.com/misTrasteos/b969f1b208375ecfe1960d6cfa0daab9)

# config.yml
**output.path**, output folder

**output.delete**, if output folder already exists, it will be deleted

**sourceRepository**, the repository directory

**distributionManagement.id**, id of the target repository. It will be used in `settings.xml` __id__ element  and in modules `pom.xml` __repositoryId__ of the _deploy:deploy-file_ goal

**distributionManagement.url**, url of the target repository. It will be used in the deploy

**distributionManagement.username**, username of the remote repository. It will be used in `settings.xml`file

**distributionManagement.password**, password for the remote repository user. It will be used in `settings.xml` file

