pipeline {
    agent any

    environment{
        DOCKER_HOST = 'tcp://host.docker.internal:2375'
        def dockerTool = tool name: 'docker-latest-tool', type: 'org.jenkinsci.plugins.docker.commons.tools.DockerTool' 
        PATH = "${dockerTool}/bin:${env.PATH}"    
    }

    stages {
        stage('Load ENV'){
            steps{
                withCredentials([file(credentialsId: 'indietour-api-env', variable: 'ENV')]){
                    sh "rm -f .env"
                    sh "cp $ENV .env"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                    docker build -t dstoffels/indietour-api-dev:latest .
                    """
                }
            }
        }

        stage('Local Compose') {
            steps {
                sh "docker-compose -f docker-compose-dev.yaml down"
                sh "docker-compose -f docker-compose-dev.yaml -p indietour-api up -d"
            }
        }
    }
}
