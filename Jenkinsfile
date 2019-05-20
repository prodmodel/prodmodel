pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt --user'
            }
        }
        stage('Test') {
            steps {
                sh 'python -m pytest tests'
            }
        }
    }
}
