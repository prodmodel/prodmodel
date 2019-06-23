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
        stage('Python unit tests') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'python -m pytest tests'
                }
            }
        }
        stage('Shell build tests') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'integration-tests/test_clean_builds__keep_lib.sh'
                }
            }
        }
        stage('Shell cleaning tests') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'integration-tests/test_cleaning.sh'
                }
            }
        }
        stage('Pylint') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'python -m pylint prodmodel --indent-string="  "'
                }
            }
        }
    }
}
