pipeline {
    agent { docker { image 'python:3.6.7' } }

    stages {
        stage('Test') {
            steps {
                sh 'python -m pytest tests'
            }
        }
    }
}
