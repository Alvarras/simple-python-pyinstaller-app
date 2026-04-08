node {
    def app

    stage('Build') {
        echo 'Building the application...'
        checkout scm

        if (isUnix()) {
            sh '''
                pip install pyinstaller
                pyinstaller --onefile sources/add2vals.py
            '''
        } else {
            bat '''
                pip install pyinstaller
                pyinstaller --onefile sources/add2vals.py
            '''
        }
        echo 'Build completed.'
    }

    stage('Test') {
        echo 'Running tests...'

        if (isUnix()) {
            sh '''
                pip install pytest
                python -m pytest sources/test_calc.py -v 2>&1 | tee test-output.txt
            '''
        } else {
            bat '''
                pip install pytest
                python -m pytest sources/test_calc.py -v
            '''
        }
        echo 'Tests completed.'
    }

    stage('Deliver') {
        echo 'Delivering artifacts...'

        if (isUnix()) {
            sh '''
                echo "=== Build Artifacts ===" > log.txt
                echo "Build Date: $(date)" >> log.txt
                echo "Pipeline: submission-cicd-pipeline" >> log.txt
                echo "" >> log.txt
                echo "=== Test Results ===" >> log.txt
                cat test-output.txt >> log.txt 2>/dev/null || echo "No test output found" >> log.txt
                ls -la dist/ >> log.txt 2>/dev/null || true
            '''
        }

        archiveArtifacts artifacts: 'log.txt', fingerprint: true
        archiveArtifacts artifacts: 'dist/*', fingerprint: true, allowEmptyArchive: true

        echo 'Delivery completed!'
    }
}
