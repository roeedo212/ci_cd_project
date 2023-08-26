def dockerImage
pipeline {
    agent {
        kubernetes {
            label 'promo-app'
            idleMinutes 5
            yamlFile 'build-pod.yaml'
            defaultContainer 'ez-docker-helm-build'
        }
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '5'))
    }

    environment {
        DOCKER_IMAGE = 'roeedot/movie-rate-repo'
        HELM_PACKAGE = 'roeedot/movie-rate-chart'
        DOCKERHUB_CREDENTIALS = credentials('docker_hub_id')
    }

    stages {
        stage('Setup') {
            steps {
                checkout scm
                script {
                    if (env.BRANCH_NAME == 'main') {
                        env.BUILD_ID = "1." + sh(returnStdout: true, script: 'echo $BUILD_NUMBER').trim()
                    } else {
                        env.BUILD_ID = "0." + sh(returnStdout: true, script: 'echo $BUILD_NUMBER').trim()
                    }
                    currentBuild.displayName += " {build-name:" + env.BUILD_ID + "}"
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
            steps {
                sh 'helm lint movie-rate-chart'
                sh 'helm package movie-rate-chart --version '+env.BUILD_ID

                }
            }

        stage('Push Docker image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker_hub_id') {
                        dockerImage.push()
                    }
                }
            }
        }

        
        stage('Push HELM chart') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker_hub_id', passwordVariable: 'DOCKERHUB_PASSWORD', usernameVariable: 'DOCKERHUB_USER')]) {
                        sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u ${DOCKERHUB_USER} --password-stdin"
                        sh 'helm push movie-rate-chart-'+env.BUILD_ID+'.tgz oci://registry-1.docker.io/roeedot'
                    }
                }
            }
        }
    }   
}
