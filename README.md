# python-ecs-api

cd src/
sh build.sh
python api.py

```bash
{"@timestamp":"2021-04-06T20:31:01.899Z","log.level":"info","message":"Info level message log in / route.","ecs":{"version":"1.6.0"},"log":{"logger":"app"}}
{"@timestamp":"2021-04-06T20:31:01.900Z","log.level":"info","message":"Creating new Client","ecs":{"version":"1.6.0"},"log":{"logger":"app"}}
{'CustomerName': 'Jake'}
{"@timestamp":"2021-04-06T20:31:01.901Z","log.level":"info","message":"Provisioned Client with ID : 6ad5b8f9-01d9-4f8e-aa18-4b085a8889b9","ecs":{"version":"1.6.0"},"log":{"logger":"app"}}
```