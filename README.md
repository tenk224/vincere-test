# vincere-test

# Question 1

## 1. Introduction

Before go deeper into the Architecture, I will break down the requirements into smaller problems or possible recommendations based on but not limited to my own knowledge at the time of writing this (I may have forgotten some important things).

## 2. Requirements

> scaling to meet the demand, but with uncertainty around when and how much this demand will be they are very concerned about buying too much infrastructure too soon or not enough too late!

- The only solution for this unpredictable demands is using **Cloud Hosting**.
- Using **Cloud Hosting** comes with some pros and cons:
  - Pros:
    - Can quickly spin up resources as the needs arise.
    - A lot of managed services -> less effort on operating, monitoring... for just a few bucks
    - Can achieve Service Level Agreements (SLA) like 99.9999999% up time.
    - Backup and restore is easier.
  - Cons:
    - Services are frequently updated so we need to keep ourselves up-to-date with the new features
    - Cloud outage impacts the business if the design is not fault tolerant (e.g. AWS outage leads to a lot of services/games outage).
    - Security on the cloud is another problem we need to take care (e.g. tool to scan our servers for exploits/vulnerabilities, scan access/secret key leaks...)
    - Need to monitor and optmize cost before it goes out of hand.
- Using **Cloud Hosting** and **on-prem Infrastructure** as the same time (hybrid infrastrucure):
  - Pros:
    - Can design for a better fault-tolerant architecture(e.g. 2 outage cloud regions and we still have the on-prem infrastructure)
    - Security policy to enforce some sensitive information to be hosted on-prem only.
  - Cons:
    - Cost of managing both environments and engineers to operate them.
    - The infrastructure becomes more complicated (e.g. traffic between the environments, DNS for both environments...)
    - All the cons of having on-prem infrastructure

**Assumptions**:

- Since the solution for this requirements is purely using cloud hosting, I will take out the on-prem solution and assume we are talking about Amazon Web Service (AWS)

> their lack of provision for Disaster Recovery

- Depends on the budget and SLA, we can go from this order:
  1. Backup and restore: low cost possible, high recovery time objective (RTO)
  2. Multi-zone: fairly low cost, medium RTO.
  3. Multi-region with active-passive: high cost, low RTO. We need ways to spin up, warm up resources (e.g. spin up more EC2 instances, scale out Database...) for the passive region when the outage is happening.
  4. Multi-region with active-active: high cost possible, lowest RTO. We need strategies for routing users' requests, design write queries for databases, consider replication lag.
  5. Multi-region with on-prem infrastructure. This is the best scenarios I can think of and have not yet had any experience to talk about it.
- Use infrastructure as code for quickly mapping resources' configurations and spin up when needed.

> their ability to configure their database and data access layer for high performance and throughput

- Scale up. As in increasing CPU/RAM for the Database.
- Scale out:
  - Use master-slave mode of the Database:
    - Since most of the applications will read more than write, the master node will execute the write queries and the slave will execute the read queries.
    - When one or more slave nodes are down, the read queries will then be shifted to the master node.
    - When the master node is down, the other slave will elect a new master.
    - Mult-master architecture is comlicated as we will need network file system for storing all masters' data and possible network lag issues.
  - Use cache to serve frequent read query's results.

> making the user experience in the browser very low latency even though a large portion of their user base will be from far away

- Frontend, static contents:
  - Use AWS s3 and cloudfront CDN:
    - S3 bucket to store the original static content.
    - Cloudfront CDN to store the content on the nearest AWS Edge Location to the user, which is fetched from the S3 bucket (same as cache).
- Backend, api response:
  - Detemine what "very low latency" is:
    - My check from [cloudping.info](https://www.cloudping.info/) ranging from 62ms for Singapore to 367ms for São Paulo.
  - Detemine where the user base is the most:
    - Something like where 80% of the users are?
  - Deploy the multi region architecture if we have the most users from **n** regions
  - Reduce reponse time from our ends:
    - Determine where the bottle necks are from tracing tools.
    - Investigate slow queries from the databases.

> effective distribution of load

- Use Load Balancer to distribute the load between the application servers.
- Deploy the api in a auto scaling group :
  - Define scaling strategies:
    - Which metrics to trigger a scale? (CPU usage, RAM usage, request rate, response time...).
    - How many resources to scale at a time.
    - How to scale in.

> a self-healing infrastructure that recovers from failed service instances

- Define the statelessness of the applications:
  - No saving files to the disks.
  - Load portion of data to ram or cache.
  - AWS Load Balancer supports stickiness connection but we need to store the user's session elsewhere in the database, not to the disks.
- Define and tune healthcheck settings for applications:
  - Either TCP or HTTP
- Base on the healthcheck status to know whether the application is running or crashed to keep it or destroy it and spin up another resources
- Have a application replica of at least 2.
- Define a policy where the destroying an instance or spin a new instance.

> security of data at rest and in transit

- Use AWS KMS to encrypt and decrypt data.
- Use AWS bucket with encryption and appropriate policies for authenticating and authorizing users who can and can do what to decrypt.

> securing access to the environment as the delivery team expands

- Deploy AWS private and public subnets.
- Deploy OpenVPN in the public subnets for accessing the resources in the private subnets.
- Having security polices enforce for the delivery team (e.g. polices for password, mfa, password retention...) 

> an archival strategy for inactive objects greater than 6 months

- Use AWS S3 Glacier.

> ability to easily manage and replicate multiple environments based on their blueprint architecture.

- Infrastructure as code (e.g. Terraform, Pulumi, Cloudformation for AWS)

## 3. Architecture

I will use the multi-region architecture on AWS

# Question 2

# Question 3

This github account, but nothing useful for reference since I don't have any contribution.

# Question 4

DevOps is to break the silos between dev team and ops team where ops people don't understand the applications' behaviour and dev people don't understand how their apps get deployed. We can discuss more if you want to go deep dive.

# Question 5

- Container runtime:
  - Docker
  - Containerd
- Container orchestration:
  - Kubernetes
- Container Network Interface:
  - Calico
- Container Storage Interface driver:
  - Rook Ceph
  - AWS EBS
- Continuous Integration:
  - Gitlab ci, Kubernetes Gitlab runner
  - Kaniko (building image within a container and skip the login to image repository)
  - Bitbucket Pipeline
  - Jenkins
- Continuous Deployment/Delivery:
  - Fluxcd (GitOps for Kubernetes):
    - Source controller: libgit2 for Bitbucket.
    - Helm controller.
    - Kustomization controller: struturing git repository.
    - Image Automation controller: update image tag to git repository.
    - Image Reflector controller: scan image repository to get new tag.
    - Notification controller: notification for Fluxcd objects like Helm Release, Image Policy...
  - Ansible
- Configuration management:
  - Ansible
- Kubernetes deployment:
  - Kubespray (collection of Ansible playbook)
  - kOps
  - Eksctl 
- Infrastructure as Code:
  - Terraform
  - Pulumi
- Cloud provider:
  - AWS
  - GCP
  - Aliyun (Alibaba cloud in mainland china)
- Monitoring/Logging/Alerting/Dashboard:
  - Prometheus
  - Grafana
  - Loki
  - Promtail
- Kuberentes auto scaling:
  - Cluster autoscaler
- Secrets for Kubernetes:
  - SealedSecret
  - Vault (researching)
- AWS IAM roles:
  - Kube2IAM
  - Kube2RAM (Aliyun)
  - IAM role for service account
  - OIDC for Bitbucket
- Kubernetes manifest template:
  - Helm

# Question 6

- Continuous Integration/Continuous Deployment/Delivery
- Already listed in the question 5. If you want to discuss deeper please take it to the interview since I don't know what depth of the aspect you are interested in.

# Question 7

- Cloud provider:
  - AWS
  - GCP
  - Aliyun (Alibaba cloud in mainland china)
  - Tencent cloud (only creat a machine)
- The one I like the most:
  - AWS
- Reasons:
  - I work with AWS the most, and AWS is fairly large and mature enough in terms of Cloud provider.
  - GCP console is so hard to self navigate, need to read documents back and forth.
  - Aliyun has a lot of bugs that I needed to contact the support team for solving the problems.
  - Have not yet used Azure.

# Question 8

- Containers are processes running on a machine which contains the packed applications and dependencies.
- Advantages:
  - Lightweight:
    - No resource overhead to init the whole operating system
    - Faster to terminate/kill
    - Only consume the required resource (CPU/RAM)
  - Isolate application environment:
    - Different applications running on different libraries/dependencies without interfering with each other on the same machine
- Disavantages:
  - Overhead for system calls since it will go through a container runtime (comparing deploying to a container on a machine or deploy directly to that same machine). But most applications will not suffer from this anyway.
- I use container in Kubernetes, Bitbucket Pipeline, Docker compose.  

# Question 9

- Migrating fluxcd version 1 to version 2.
- My role was the project owner.
- The project has some positive outcomes:
  - Restruturing git repository for other team rather than the DevOps team to manage Kubernetes resources/custom resources. We have different git repository for different namespaces/teams.
  - Moving away from the deprecated flux version 1.
  - Enhance the team knowledge of reading Go toolkit components, reading Go lang codes to configure the custom resources.

# Question 10

- Deploy the database servers in the Database subnet (same as private subnet but with Network ACL that allow only connection on the port of the Database)
- Resize this Database subnet for only a few IPs (e.g. with /26 or /27) that could obtain since we don't want anyone to deploy more Database rather than we are currently using.
- Security groups for allowing connections from the applications.

# Question 11

- Not yet, please enlighten me.

# Question 12

- I have a mindset of continuous learning, doubting my own knowledge to keep these in check and up-to-date. If those sound like you, I maybe the one you need.