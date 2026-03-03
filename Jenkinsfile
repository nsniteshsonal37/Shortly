pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Pull Latest') {
            steps {
                sh 'git pull origin main'
            }
        }

        stage('Rebuild Containers') {
            steps {
                sh 'docker-compose up -d --build'
            }
        }
    }
}
