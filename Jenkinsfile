pipeline {
    agent any
    
    environment {
        APP_URL = 'http://13.51.159.98:5173'
        API_URL = 'http://13.51.159.98:5000'
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/ShahabHassanK/selenium-tests-employee-mgmt.git'
            }
        }
        
        stage('Run Tests with Selenium Grid') {
            steps {
                script {
                    // Use docker compose to orchestrate Selenium Grid and tests
                    sh 'docker compose up --build --abort-on-container-exit --exit-code-from tests'
                }
            }
            post {
                always {
                    // Copy report from container
                    sh 'docker cp $(docker compose ps -q tests):/app/report.html . || true'
                    // Clean up containers
                    sh 'docker compose down -v'
                }
            }
        }
        
        stage('Archive Results') {
            steps {
                // Publish HTML report
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: '.',
                    reportFiles: 'report.html',
                    reportName: 'Selenium Test Report'
                ])
            }
        }
    }
    
    post {
        always {
            // Send email notification
            emailext (
                subject: "Test Results: ${currentBuild.fullDisplayName}",
                body: """
                    <h2>Build Status: ${currentBuild.result}</h2>
                    <p><b>Build Number:</b> ${env.BUILD_NUMBER}</p>
                    <p><b>Build URL:</b> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                    <p><b>Test Report:</b> <a href="${env.BUILD_URL}Selenium_Test_Report/">View Report</a></p>
                    <hr>
                    <p>Triggered by: ${env.GIT_COMMITTER_EMAIL}</p>
                """,
                to: 'shahab.hassan2020@gmail.com',
                mimeType: 'text/html',
                attachLog: true
            )
        }
        success {
            echo 'All tests passed! ✅'
        }
        failure {
            echo 'Some tests failed! ❌'
        }
    }
}