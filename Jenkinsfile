pipeline {
    agent any

    environment {
        NODE_ENV = 'production'
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building the project'
                sh 'npm install'
                sh 'npm run build'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests'
                sh 'npm test'
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                echo 'Deploying the application'
                sh 'npm run deploy'
            }
        }
    }

    post {
        always {
            echo 'Cleaning up after the pipeline'
            cleanWs()
        }
    }
}
