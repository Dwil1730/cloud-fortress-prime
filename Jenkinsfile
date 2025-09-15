pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "dwil1730/flask-app:latest"      // Your DockerHub image
        DOCKER_CREDENTIALS = "dockerhub-creds"         // Jenkins credential ID for DockerHub
        GITHUB_REPO = "https://github.com/Dwil1730/cloud-fortress-prime.git"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: "${env.GITHUB_REPO}"
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${env.DOCKER_IMAGE}")
                }
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker run --rm ${DOCKER_IMAGE} pytest'
            }
        }

        stage('Security Scan (Trivy)') {
            when { expression { fileExists('Dockerfile') } }
            steps {
                sh 'trivy image ${DOCKER_IMAGE}'
            }
        }

        stage('Push Docker Image') {
            steps {
                withDockerRegistry([ credentialsId: "${env.DOCKER_CREDENTIALS}", url: '' ]) {
                    sh "docker push ${env.DOCKER_IMAGE}"
                }
            }
        }

        stage('Deploy to Staging') {
            steps {
                sh 'docker-compose -f docker-compose.staging.yml up -d'
            }
        }

        stage('Manual Approval for Production') {
            steps {
                input message: 'Deploy to Production?'
            }
        }

        stage('Deploy to Production') {
            steps {
// @ something
