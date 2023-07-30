pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("dstoffels/indietour-api:${env.BUILD_ID}")
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
