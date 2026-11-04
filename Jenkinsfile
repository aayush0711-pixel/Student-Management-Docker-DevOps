
pipeline {
    agent any

    environment {
        MYSQL_USER = 'studentuser'
        MYSQL_DATABASE = 'studentdb'
        MYSQL_PASSWORD = credentials('mysql-password')
        MYSQL_ROOT_PASSWORD = credentials('mysql-root-password')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo 'Code downloaded from GitHub'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t student-management-app .'
            }
        }

        stage('Deploy Application') {
            steps {
                bat 'docker-compose up -d --build'
            }
        }

        stage('Verify Deployment') {
            steps {
                bat 'docker-compose ps'
            }
        }
    }
}
