pipeline {
    agent {
        docker {
            image 'python:3.6.7'
        }
    }
    stages {
        stage('Setup') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'pip install -r requirements.txt --user'
                }
            }
        }
        stage('Test') {
            steps {
                sh 'python -m pytest tests'
            }
        }
    }
}
