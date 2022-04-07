Welcome to the consensus challenge. This playground project contains the following scenario:



Nodes: Contains the logic of the system. All the nodes can write the operations into one file(the database) and perform the operations. The leader is in charge of replicating the data into the rest of nodes. A node can also answer a read and 

Orchestrator: this piece operates like a custom simplified ingress. It sends the writes to all the nodes and the reads to a random node. 
## How to run it
First start minikube environment:
`minikube start`
Then run the following command to be able to deploy the images on minikube:
`eval $(minikube docker-env)`
Run tunnel to expose orchestrator
`minikube tunnel`

## How to deploy it

Basically we need to deploy two things, nodes and orchestrator. For hat wee have to run some make commands:

- Build the nodes code
`make build-node`
- Build the orchestrator code
`make build-orchestrator`

- Deploy nodes
`make deploy-nodes`
- Deploy orchestrator
`make deploy-orchestrator`

The orchestrator sets the leader on the beginning so we must ensure that it starts after the nodes. To be sure we can restart the orchestrator after deploying it:
`make restart-orchestrator`

## Useful info
The volumes that we use for the node database are permanent. Which means that they are alive after the nodes died. If we want to start the problem from scratch we can clear the data using the following make call:

`make clear`


## How to access nodes

You can access nodes terminal by using the following command
`kubectl exec --stdin --tty $(kubectl get pod -l app=<NAME> -o jsonpath="{.items[0].metadata.name}") -- /bin/bash`

Where NAME is node1, node2, node3 or orchestrator depending on the pod you want to access 
