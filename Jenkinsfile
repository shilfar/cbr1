pipeline {
	agent any
	    stages {
	        stage('Clone Repository') {
	        /* Cloning the repository to our workspace */
	        steps {
	        checkout scm
	          }
                }
                stage ('sonarqube test') {
                   when {
                       branch 'main'
                   }
                   steps {
                       withSonarQubeEnv('sonarqube') {
                         
                             sh """
				${tool("sonarqube")}/bin/sonar-scanner \
				-D sonar.login=admin \
                                -D sonar.password=admin \
                                -D sonar.projectKey=sonarqubetest \
				-D sonar.sources=/var/lib/jenkins/workspace/sonarqube-jenkinspipeline/ \
                                -D sonar.host.url=http://localhost:9000/
				"""
                       }
                
                   }
                }

                stage("quality gate") {
		    when {
                        branch 'main'
                    }
                    steps {
                       timeout(time: 5, unit: 'MINUTES') {
                       waitForQualityGate abortPipeline: true
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
                    
                    sh 'docker tag cbr-front:$BUILD_NUMBER  umarta1/cbr-front:$BUILD_NUMBER'
                    sh '''
                        docker push umarta1/cbr-front:$BUILD_NUMBER
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
