node {
    def app

    stage('Build') {
        echo 'Building the application...'
        checkout scm

        docker.image('python:3.9-slim').inside('--user root') {
            sh '''
                apt-get update && apt-get install -y binutils
                pip install --break-system-packages pyinstaller
                pyinstaller --onefile sources/add2vals.py
            '''
        }
        echo 'Build completed.'
    }

    stage('Test') {
        echo 'Running tests...'

        docker.image('python:3.9-slim').inside('--user root') {
            sh '''
                pip install --break-system-packages pytest
                python -m pytest sources/test_calc.py -v 2>&1 | tee test-output.txt
            '''
        }
        echo 'Tests completed.'
    }

    stage('Deliver') {
        echo 'Delivering artifacts...'

        sh '''
            echo "=== Build Artifacts ===" > log.txt
            echo "Build Date: $(date)" >> log.txt
            echo "Pipeline: submission-cicd-pipeline" >> log.txt
            echo "" >> log.txt
            echo "=== Test Results ===" >> log.txt
            cat test-output.txt >> log.txt 2>/dev/null || echo "No test output found" >> log.txt
            ls -la dist/ >> log.txt 2>/dev/null || true
        '''

        archiveArtifacts artifacts: 'log.txt', fingerprint: true
        archiveArtifacts artifacts: 'dist/*', fingerprint: true, allowEmptyArchive: true

        echo 'Delivery completed!'
    }
}
