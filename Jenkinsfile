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
           withCredentials([string(credentialsId: 'DOCKER_HUB_PASSWORD', variable: 'PASSWORD')]) {
                sh 'docker login -u umarta1 -p $PASSWORD'
           }

           stage("Push Image to Docker Hub"){
                sh 'docker push cbr-front:$BUILD_NUMBER'
           }

    }
}
