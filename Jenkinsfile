@Library('EZJEL') _
def dockerImage
pipeline {
    agent {
        kubernetes {
        label 'ez-joy'
        idleMinutes 5
        yamlFile 'build-pod.yaml'
        defaultContainer 'ez-docker-helm-build'
        }
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '5'))
    }

    environment {
        DOCKER_IMAGE = 'roeedot/movie_rating'
    }

    stages {
        stage('Setup') {
            steps {
                checkout scm
                script {
                    ezEnvSetup.initEnv()
                    def id = ezUtils.getUniqueBuildIdentifier()
                    if(BRANCH_NAME == 'main')
                    {
                        env.BUILD_ID = "1."+id
                    }
                    else {
                        env.BUILD_ID = "0." + ezUtils.getUniqueBuildIdentifier("issueNumber") + "." + id
                    }
                    currentBuild.displayName+=" {build-name:"+env.BUILD_ID+"}"
                }
            }
        }

        stage('Build Docker image') {
            steps {
                script {
                    dockerImage = docker.build(DOCKER_IMAGE+":"+env.BUILD_ID,"--no-cache .")
                }
            }
        }

        stage('Push Docker image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub_id') {
                        dockerImage.push()
                    }
                }
            }
        }
    }
}
