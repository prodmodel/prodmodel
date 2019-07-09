pipeline {
    agent {
        docker {
            image 'python:3.5'
        }
    }
    environment {
        AWS_ACCESS_KEY_ID     = credentials('jenkins-aws-secret-key-id')
        AWS_SECRET_ACCESS_KEY = credentials('jenkins-aws-secret-access-key')
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
                    sh 'rm -rf .target'
                    sh 'rm -rf example/.target'
                    sh 'python -m pytest tests'
                }
            }
        }
        stage('Shell build tests') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'integration-tests/test_clean_builds__keep_lib.sh'
                    sh 'integration-tests/test_output_format.sh'
                    sh 'integration-tests/test_deploy.sh'
                    sh 'integration-tests/test_external_data.sh'
                    sh 'integration-tests/test_s3_builds.sh'
                    sh 'integration-tests/test_target_dir.sh'
                    sh 'integration-tests/test_ls.sh'
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
