node {

    stage('Build') {
        echo '=== STAGE: Build ==='
        checkout scm

        docker.image('python:3.9-slim').inside('--user root') {
            sh '''
                rm -rf build dist *.spec __pycache__ .pytest_cache build-info.txt test-results.txt test-output.txt render-response.txt log.txt
                touch build-info.txt
                apt-get update && apt-get install -y binutils
                pip install --break-system-packages pyinstaller
                pyinstaller --onefile sources/add2vals.py
                echo "Build selesai: $(date)" > build-info.txt
                ls -la dist/
            '''
            sh 'chown -R 1000:1000 . 2>/dev/null || chmod -R 777 . 2>/dev/null || true'
        }

        echo 'Build berhasil.'
    }

    stage('Test') {
        echo '=== STAGE: Test ==='

        docker.image('python:3.9-slim').inside('--user root') {
            sh '''
                touch test-results.txt
                pip install --break-system-packages pytest
                python -m pytest sources/test_calc.py -v 2>&1 | tee test-results.txt
                echo "Test selesai: $(date)" >> build-info.txt
            '''
            sh 'chown -R 1000:1000 . 2>/dev/null || chmod -R 777 . 2>/dev/null || true'
        }

        echo 'Semua test lulus.'
    }

    stage('Manual Approval') {
        echo '=== STAGE: Manual Approval ==='

        input message: 'Lanjutkan ke tahap Deploy?',
              ok: 'Proceed'

        echo 'Approved. Melanjutkan ke Deploy...'
    }

    stage('Deploy') {
        echo '=== STAGE: Deploy ==='

        sh '''
            echo "Deploy dimulai: $(date)" > build-info.txt
            echo "Aplikasi: add2vals" >> build-info.txt
            echo "Binary: dist/add2vals" >> build-info.txt
        '''

        withCredentials([string(credentialsId: 'RENDER_DEPLOY_HOOK_URL', variable: 'RENDER_HOOK')]) {
            sh '''
                echo "Triggering deploy ke Render..."
                curl -s -w "\\nHTTP_CODE:%{http_code}" -X POST "$RENDER_HOOK" -H "Content-Type: application/json" | tee render-response.txt
                HTTP_CODE=$(tail -1 render-response.txt | grep -o 'HTTP_CODE:[0-9]*' | cut -d: -f2)
                if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "201" ]; then
                    echo "Deploy hook berhasil (HTTP $HTTP_CODE)"
                else
                    echo "Deploy hook gagal atau tidak valid (HTTP $HTTP_CODE)"
                fi
                echo "Deploy response: $(grep -v 'HTTP_CODE:' render-response.txt)" >> build-info.txt
            '''
        }

        echo 'Deploy trigger selesai.'
        echo 'Menjeda pipeline selama 60 detik agar aplikasi berjalan...'

        sh 'sleep 60'

        echo 'Waktu 60 detik habis. Pipeline selesai.'

        sh '''
            echo "=============================" > log.txt
            echo "  PIPELINE EXECUTION REPORT  " >> log.txt
            echo "=============================" >> log.txt
            echo "Tanggal  : $(date)" >> log.txt
            echo "Pipeline : ${JOB_NAME} #${BUILD_NUMBER}" >> log.txt
            echo "" >> log.txt
            echo "--- Build Info ---" >> log.txt
            cat build-info.txt >> log.txt
            echo "" >> log.txt
            echo "--- Test Results ---" >> log.txt
            if [ -f test-results.txt ]; then
                cat test-results.txt >> log.txt
            else
                echo "No test results available" >> log.txt
            fi
            echo "" >> log.txt
            echo "--- Render Deploy Response ---" >> log.txt
            if [ -f render-response.txt ]; then
                cat render-response.txt >> log.txt
            else
                echo "No deploy response available" >> log.txt
            fi
            echo "" >> log.txt
            echo "Status: SUCCESS" >> log.txt
        '''

        archiveArtifacts artifacts: 'log.txt', fingerprint: true
        archiveArtifacts artifacts: 'dist/*', fingerprint: true, allowEmptyArchive: true
    }
}