# CI/CD Basic Knowledge

My practice of CI/CD.

## What is CI/CD

    CI/CD is called: Continuous Integration and Continuous Deployment. This is a process of how to publish code to an env automatic and it have several kinds of way to deal that:
    * GitHub Actions
    * Jenkins
    * other ways

    This document we just using GitHub Actions to deal with that. I will give you a full process of public the project of Python Django.
    After that, we will deploy the image we generated to K8S. Running on the K8S normally, then we can visit our program outside as a user. 

## CI/CD

    * start an github repos at the Github pages, we call it my-cicd
    * Click Action tab in the main page of the repos in Github, we can choose Django to
    * .github/workflow/django.yaml will be appeal in our project
    * read the content of this file, we can see that all the struct has been finished.

## CI

    let's CI!

1. Content of That Yaml
    basic it will have four parts of that file:
    * name: name of the project
    * on: what actio    n it can be on this project (push, pull_request etc.)
    * jobs: this is the most complicated part of this file, just define different step of the action while will be done on the process
    * jobs/build : here you can define different actions to doing something you want. and it depend on what action name you defined, such as "- uses: actions/checkout@v4", that means you need to execute the logic define in the action's checkout at the ver 4. jobs/build have different other attribute.
    * jobs/build/runs-on: that means that what's the main docker image your project will running on.
    * jobs/build/strategy : define the attribute of the project
    * jobs/build/steps: is defined all the step it will execute while we using CI/CD, this part is most important. each command line will start with "- ". It based on the action and action arguments.
    * jobs/build/run: define the shell command will run in the docker instance

    * this is a example of that file :
        ```yaml
        name: Django CI

        on:
            push:
                branches: [ "main" ]
            pull_request:
                branches: [ "main" ]

        jobs:
            build:
                runs-on: ubuntu-latest
                strategy:
                    max-parallel: 4
                    matrix:
                        python-version: [3.7, 3.8, 3.9]

                steps:
                - uses: actions/checkout@v4
                - name: Set up Python ${{ matrix.python-version }}
                uses: actions/setup-python@v3
                with:
                    python-version: ${{ matrix.python-version }}
                - name: Install Dependencies
                run: |
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                - name: Run Tests
                run: |
                    python manage.py test

        ```

    If the pull_request defined branches does not include what branch you send pull_request, the error will be happened.

    and you can see the output from Docker Image management tool.

2. All Actions
    * you can visit the URL: "https://www.github.com/actions" to get all actions pre-defined by the open source world.
    different kinds of action will do different things you can use that yaml to finish what you want. and if you want know what is the main logic of that action, you can read that file there.
    It has the document there, you can read that while you confused

3. How to make Docker Image
    * you can go to the docker hub and Repository to restore the docker for one project. https://hub.docker.com/repositories/gordenfl
    * create an Repository at this time we call it 'gordenfl'
    * bind docker with github:
        * you need create environment variable in the setting page of your code repository on the github:

            ```path
                setting->Secrets and variables -> Actions
            ```

            here we can see the repository secret, create two of them:

            ```shell
                DOCKER_USERNAME: XXXXXXX
                DOCKER_PASSWORD: XXXXXXX
            ```

        * we can generate our Docker image with our config file with append the next content to the tail of yaml file:

            ```yaml
            - name: Build and Push Docker Image
                uses: mr-smithers-excellent/docker-build-push@v6
                    #docer login dckr_pat_d08Rgg754QgnH5fpC6yJAjcqMDg
                with:
                    image: gordenfl/tttt # come from hte docker hub, what dockerhub repositories you want put
                    tags: v1, latest
                    registry: docker.io   # 如果是推送到docker Hub 的话,这里必须要写docker.io, 否则会有问题
                    dockerfile: Dockerfile.ci
                    username: ${{ secrets.DOCKER_USERNAME }} # 这定义在github里面 本项目的Setting里面有一个环境变量定义的功能
                    password: ${{ secrets.DOCKER_PASSWORD }} # 也是但是不要配置错误
            ```

            this will let github actions to make a docker image and upload to DockerHub. So when you commit and pull_request code to the github, this logic will be triggered the Docker image will be updated.

        After that docker and github repository has been bind together. Anytime while you commit code, the Docker image will be generated.

## CD

    Let's CD right now!!

1. All explanation of 1 2 3 are all the CI (Continuous Integration) part of CI/CD. next step we need explain what is CD (Continuous Delivery).

    * What's the Delivery, that means we need to send our docker images to user, let them use all the new function or bug fixing.

2. How to deploy the Docker image into K8S.
    * You should install MiniKube in you platform. if don't know how to, please check the Document of K8S/INSTALL.md
    * Assume you have start the minikube. While





















kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: gordenfl-token
  annotations:
    kubernetes.io/service-account.name: gordenfl
type: kubernetes.io/service-account-token
EOF



- name: Update deployment
  uses: appleboy/kubernetes-action@master
  with:
    server: ${{ secrets.K8S_SERVER }}
    ca_cert: ${{ secrets.K8S_CA_CERT }}
    token: ${{ secrets.K8S_TOKEN }}
    namespace: github-action
    deployment: nginx
    container: nginx
    image: nginx:1.24.0


在上述配置中：

server：Kubernetes 集群的 API 服务器地址。

ca_cert：证书颁发机构的证书。

token：用于认证的 Kubernetes 服务账户令牌。

namespace：指定的命名空间。

deployment：要更新的部署名称。

container：要更新的容器名称。

image：新的镜像名称和标签。


kubectl config view --minify -o jsonpath='{.clusters[0].cluster.certificate-authority}'
cat ~/.minikube/ca.crt | base64 -w 0





