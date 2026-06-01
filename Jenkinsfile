pipeline {
    agent any

    // Shared values for all stages. ${BUILD_NUMBER} is injected by Jenkins automatically.
    environment {
        IMAGE_NAME     = 'ci-cd-jenkins-demo'
        CONTAINER_NAME = 'ci-cd-demo'
        HOST_PORT      = '8000'
        CONTAINER_PORT = '5000'
    }

    options {
        // Don't let a hung run wedge Jenkins forever.
        timeout(time: 10, unit: 'MINUTES')
        // Keep console output readable.
    }

    stages {

        stage('Build') {
            steps {
                echo "Building image ${IMAGE_NAME}:${BUILD_NUMBER}"
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .'
            }
        }

        stage('Test') {
            steps {
                echo "Running pytest inside ${IMAGE_NAME}:${BUILD_NUMBER}"
                sh 'docker run --rm ${IMAGE_NAME}:${BUILD_NUMBER} pytest -v'
            }
        }

        stage('Deploy') {
            steps {
                echo "Deploying ${IMAGE_NAME}:${BUILD_NUMBER} as container ${CONTAINER_NAME}"
                // Remove the previous container if it exists. `|| true` so the first ever run does not fail.
                sh 'docker rm -f ${CONTAINER_NAME} || true'
                sh '''
                    docker run -d \
                      --name ${CONTAINER_NAME} \
                      -e BUILD_NUMBER=${BUILD_NUMBER} \
                      -p ${HOST_PORT}:${CONTAINER_PORT} \
                      ${IMAGE_NAME}:${BUILD_NUMBER}
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline succeeded. App is reachable at http://127.0.0.1:${HOST_PORT}"
        }
        failure {
            echo "❌ Pipeline failed. Check the failed stage logs above."
        }
    }
}