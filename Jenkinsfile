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
        DOCKER_IMAGE = 'yakirlevi11/movie-rate-repo'
        HELM_PACKAGE = 'yakirlevi11/movie-rate-repo'
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
        

        stage("Build Helm chart") {
            when {
                branch 'main'
            }
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub', passwordVariable: 'DOCKERHUB_PASSWORD', usernameVariable: 'DOCKERHUB_USER')]) {
                        sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u ${DOCKERHUB_USER} --password-stdin"
                        sh 'helm push movie-rate-chart'+env.BUILD_ID+'.tgz oci://registry-1.docker.io/yakirlevi11'
                    }
                }
            }

        }

        stage('Push Docker image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker_hub1') {
                        dockerImage.push()
                    }
                }
            }
        }

        
        stage('Push HELM chart') {
            when {
                branch 'main'
            }
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub', passwordVariable: 'DOCKERHUB_PASSWORD', usernameVariable: 'DOCKERHUB_USER')]) {
                        sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u ${DOCKERHUB_USER} --password-stdin"
                        sh 'helm push movie-rate-repo'+env.BUILD_ID+'.tgz oci://registry-1.docker.io/yakirlevi11'
                    }
                }
            }

    }   
}
