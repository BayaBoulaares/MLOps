pipeline {
    agent any
    environment {
        DOCKERHUB = credentials('dockerhub-username') // ID du credential
    }
    stages {
        stage('Test Credentials') {
            steps {
                script {
                    echo "Username: $DOCKERHUB_USR"
                    // Ne jamais echo le password dans un vrai pipeline !
                }
            }
        }
    }
}
