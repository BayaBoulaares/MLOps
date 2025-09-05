pipeline {
    agent any

    environment {
        APP_NAME = "mlops-flask-app"
        DOCKERHUB = credentials('baya-dockerhub') // ID Jenkins Credential (username + password)
        DOCKER_IMAGE = "${DOCKERHUB_USR}/${APP_NAME}:latest"
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "➡️ Building Docker image with multi-stage..."
                    DOCKER_BUILDKIT=1 docker build -t $APP_NAME .
                '''
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                sh '''
                    echo "➡️ Pushing image to Docker Hub..."
                    echo "$DOCKERHUB_PSW" | docker login -u "$DOCKERHUB_USR" --password-stdin
                    docker tag $APP_NAME $DOCKER_IMAGE
                    docker push $DOCKER_IMAGE
                    docker logout
                '''
            }
        }

        stage('Deploy (if docker-compose.yml exists)') {
            when { expression { return fileExists('docker-compose.yml') } }
            steps {
                sh '''
                    echo "➡️ Deploying with Docker Compose..."
                    docker compose pull
                    docker compose up -d --force-recreate
                '''
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo "✅ Pipeline finished successfully!"
        }
        failure {
            echo "❌ Pipeline failed!"
        }
    }
}
