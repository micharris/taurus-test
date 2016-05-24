cd var/lib/taurus/
curl -H 'Authorization: token 6cc4e6f944c47306538f5a59e878a9e4e90150d6' -H 'Accept: application/vnd.github.v3.raw' https://api.github.com/repos/micharris/contents/taurus-test/load_test.yml > load_test.yml 
curl -H 'Authorization: token 6cc4e6f944c47306538f5a59e878a9e4e90150d6' -H 'Accept: application/vnd.github.v3.raw' https://api.github.com/repos/micharris/contents/taurus-test/load_test.py > load_test.py 
curl -H 'Authorization: token 6cc4e6f944c47306538f5a59e878a9e4e90150d6' -H 'Accept: application/vnd.github.v3.raw' https://api.github.com/repos/micharris/contents/taurus-test/datadog.json > datadog.json 

python data_dog_event.py start

bzt load_test.yml 

python data_dog_event.py end
python load_test_parser.py
python load_test_to_csv.py

curl -i -H "x-api-key:HU2B/v4BMSIcjJxkF8aQ/jwGJlvKHElqh2Y4ZpyXDWA=" --upload-file responseTime.csv http://artifactory.gannettdigital.com/artifactory/load-test-results/%teamcity.project.id%/responseTime/responseTime-$(date +%s).csv
curl -i -H "x-api-key:HU2B/v4BMSIcjJxkF8aQ/jwGJlvKHElqh2Y4ZpyXDWA=" --upload-file errorRate.csv http://artifactory.gannettdigital.com/artifactory/load-test-results/%teamcity.project.id%/errorRate/errorRate-$(date +%s).csv

python %teamcity.agent.work.dir%/load-test-aggregate-results.py %X-API-KEY% %teamcity.project.id% responseTime %teamcity.agent.work.dir% %API_KEY%
python %teamcity.agent.work.dir%/load-test-aggregate-results.py %X-API-KEY% %teamcity.project.id% errorRate %teamcity.agent.work.dir% %API_KEY%

python graphResponseTime.py
python graphErrorRate.py