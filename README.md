
### Mostly hacking on example code by 
https://github.com/saasscaleup/openai-assistant 

Mad respect. Give him a subscribe on Youtube (https://youtu.be/yhASXY6rbjo?si=ECuWflcaVQS4o4Io)


### To deploy to Digital Ocean App Platform

Run `poetry export --without-hashes --format=requirements.txt > requirements.txt`

Add `streamlit run app.py --server.port 8080 --server.headless true` to the App Settings > App Spec > `run` value in the YAML file

