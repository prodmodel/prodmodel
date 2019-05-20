pipeline {
    agent { docker { image 'python:3.6.7' } }

    stages {
        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh 'python -m pytest tests'
            }
        }
    }
}
