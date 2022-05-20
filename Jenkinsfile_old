pipeline {
	agent any
            environment {
                ENV_BRNAME = "${env.BRANCH_NAME == "main" ? "prod" : "dev"}"
		    }

	    stages {
	        stage('Clone Repository') {
	        /* Cloning the repository to our workspace */
	        steps {
	        checkout scm
	          }
                }
                stage ('sonarqube test') {
                   steps {
                       withSonarQubeEnv('sonarqube') {
                         
                             sh """
				${tool("sonarqube")}/bin/sonar-scanner \
				-Dsonar.login=admin \
                                -Dsonar.password=admin1 \
                                -Dsonar.projectKey=sonarqubetest \
				-Dsonar.sources=/var/lib/jenkins/workspace/sonarqube-jenkinspipeline/ \
                                -Dsonar.host.url=http://localhost:9000/
				
                             """
                       }
                
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
                    
                    sh 'docker tag cbr-front:$BUILD_NUMBER  umarta1/cbr-front:latest'
                    sh '''
                        docker push umarta1/cbr-front:latest
                    '''
                    }
                }
           }

           stage('Pull the latest docker image from DockerHub') {
                steps{
                withDockerRegistry(credentialsId: 'dockerhub-cbr', url: 'https://index.docker.io/v1/') {
                    
                    sh '''
                        docker pull umarta1/cbr-front:latest
                    '''
                    sh 'docker tag umarta1/cbr-front:latest  cbr-front:$BUILD_NUMBER'
                    }
                }
           }

           stage('Delete docker image locally') {
                steps{
                    sh 'docker rmi cbr-front:$BUILD_NUMBER'
                }
           }
           
           stage('Deploy cbr1app') {
              steps {
                dir('deploy') {
                    sh 'kubectl apply -f deploy-front-${ENV_BRNAME}.yaml --namespace=${ENV_BRNAME}'
                    sh 'kubectl get svc --namespace=${ENV_BRNAME}'
                    sh 'kubectl get pods -n ${ENV_BRNAME} -o wide'
                    sh 'kubectl rollout restart deployment cbr1app-deploy-${ENV_BRNAME} -n ${ENV_BRNAME}'
                    sh 'kubectl get svc --namespace=${ENV_BRNAME}'
                    sh 'kubectl get pods -n ${ENV_BRNAME} -o wide'
                }
            }
        }


     }
}
