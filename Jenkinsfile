pipeline {
	agent any
	    stages {
	        stage('Clone Repository') {
	        /* Cloning the repository to our workspace */
	        steps {
	        checkout scm
	        }

	   }
	   stage('Build Image') {
	        steps {
                sh 'sudo docker build -t cbr-front:$BUILD_NUMBER .'
	        }
	   }
	   stage('Run Image') {
	        steps {
	        sh 'sudo docker run -d -p 5000:5000 --name cbr-front cbr-front:$BUILD_NUMBER'
	        }
	   }
	   stage('Testing'){
	        steps {
	            echo 'Testing..'
	            }
	   }
           stage('Push docker image to DockerHub') {
                steps{
                withDockerRegistry(credentialsId: 'dockerhub-cbr', url: 'https://index.docker.io/v1/') {
                    sh '''
                        docker push cbr-front:$BUILD_NUMBER
                    '''
                    }
                }
           }
           stage('Delete docker image locally') {
                steps{
                    sh 'docker rmi cbr-front:$BUILD_NUMBER'
                }
           }
     }
}
