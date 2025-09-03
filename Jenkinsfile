pipeline {
  agent any
  environment {
    DOCKERHUB_CREDENTIALS = credentials('dockerhub-username') // ID du credential Jenkins
    APP_NAME = "mlops-flask-app"
    DOCKER_IMAGE = "${DOCKERHUB_CREDENTIALS_USR}/${APP_NAME}:latest"
  }

  stages {
    stage('Login & Push Docker Image') {
      steps {
        sh '''
          echo "$DOCKERHUB_CREDENTIALS_PSW" | docker login -u "$DOCKERHUB_CREDENTIALS_USR" --password-stdin
          docker build -t ${DOCKER_IMAGE} .
          docker push ${DOCKER_IMAGE}
          docker logout
        '''
      }
    }
  }
}
