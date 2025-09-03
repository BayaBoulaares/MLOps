pipeline {
  agent any

  environment {
    APP_NAME = "mlops-flask-app"
    // Ici, on récupère le credential Jenkins (username/password)
    DOCKERHUB = credentials('dockerhub-username') 
    // DOCKERHUB_USR et DOCKERHUB_PSW sont automatiquement disponibles
    DOCKER_IMAGE = "${DOCKERHUB_USR}/${APP_NAME}:latest"
  }

  stages {
    stage('Login, Build & Push Docker Image') {
      steps {
        script {
          sh '''
            # Connexion à Docker Hub
            echo "$DOCKERHUB_PSW" | docker login -u "$DOCKERHUB_USR" --password-stdin

            # Build de l'image
            docker build -t ${DOCKER_IMAGE} .

            # Push de l'image
            docker push ${DOCKER_IMAGE}

            # Déconnexion
            docker logout
          '''
        }
      }
    }
  }
}
