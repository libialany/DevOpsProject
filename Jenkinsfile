node {
    def application = 'helloworld'
    def dockerhubaccountid = "libiamel"
    stage('Clone repository') {
        checkout scm
    }
    stage('Build image') {
        app = docker.build("${dockerhubaccountid}/${application}:${BUILD_NUMBER}")
    }
    stage('Push image') {
        withDockerRegistry([ credentialsId: "dockerHub", url: "" ]) {
		app.push()
		app.push("latest")
	}
    }
    stage('Deploy') {
        sh "docker run -d -p 3333:3333 ${dockerhubaccountid}/${application}:${BUILD_NUMBER}"
    }
    stage('Remove old image') {
        sh "docker rmi ${dockerhubaccountid}/${application}:latest -f"
    }
}