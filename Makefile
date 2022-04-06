SHELL := /usr/bin/env bash

###########
# Shortcuts
###########
deploy-nodes:
	for node in node1 node2 node3 ; do \
		export node ; \
		envsubst < node/k8s.yaml | kubectl apply -f -  ; \
	done
show:
	for node in node1 node2 node3 ; do \
		export node ; \
		envsubst < node/k8s.yaml | cat - ; \
	done
build-node:
	docker build -t node-consensus node/
build-orchestrator:
	 docker build -t orchestrator-consensus orchestrator/

restart-nodes:
	for node in node1 node2 node3 ; do \
		export node ; \
		kubectl rollout restart deployment $$node; \
	done
restart-orchestrator:
	kubectl rollout restart deployment orchestrator; \

run-clients:
	python client/main.py &
	python client/main.py &
	python client/main.py &
	wait
restart-all: restart-nodes restart-orchestrator
clear:
	curl http://127.0.0.1:80/clear