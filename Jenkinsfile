pipeline {
    agent any

    environment{
        DOCKER_HOST = 'tcp://docker.for.win.localhost:2375'
        def dockerTool = tool name: 'docker-latest-tool', type: 'org.jenkinsci.plugins.docker.commons.tools.DockerTool' 
        PATH = "${dockerTool}/bin:${env.PATH}"    
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                    docker build -t dstoffels/indietour-api:$BUILD_NUMBER .
                    """
                }
            }
        }

        stage('Local Compose') {
            steps {
                sh "docker-compose down"
                sh "docker-compose -f docker-compose-dev.yaml -p indietour-api up"
            }
        }
    }
}
