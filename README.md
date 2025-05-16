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
    * Assume you have start the minikube. And It can be visited on the public network. then we can let GitHub Actions to deploy the docker image to your K8S server. After that, the CD is finished.

    ```yaml
    deploy:
    needs: build #make a dependence of build. Deploy can be start only after build finished
    runs-on: ubuntu-latest #base on ubuntu
    steps:
      - name: Checkout code # check code
        uses: actions/checkout@v4

      - name: Set up kubectl #install kubectl with the version of 1.27.0
        uses: azure/setup-kubectl@v3 # the v3 means to this action's version
        with:
          version: 'v1.27.0'
      
      - name: Set up Kube config
        run: |
          mkdir -p $HOME/.kube
          echo "${{ secrets.KUBECONFIG }}" > kubeconfig.yaml
          export KUBECONFIG=kubeconfig.yaml
      
      - name: Deploy to Kubernetes
        uses: appleboy/kubernetes-action@v0.0.1 # this action can help us to distribute the Docker image to k8s
        with:
          server: ${{ secrets.K8S_SERVER }} # K8S's Master server IP
          ca_cert: ${{ secrets.K8S_CA_CERT }} # K8S's CA, you can get with next step, I will told you how to.
          token: ${{ secrets.K8S_TOKEN }} # K8S's User Token, I will told you how to .
          namespace: default
          deployment: my-app
          container: my-app
          image: ${{ secrets.DOCKER_USERNAME }}/my-app:${{ github.sha }} # Docer User name. github.sha is the latest version's hash value.
    ```

3. In the previous section, there are some value defined:

    * server：Kubernetes Cluster's Master server IP, that means  APIs Module。
    * ca_cert：Kubernetes will be assign a certification from some organization, you need get the cert's Conent with:

        ```shell
            kubectl config view --minify -o jsonpath='{.clusters[0].cluster.certificate-authority}'
            cat ~/.minikube/ca.crt | base64 -w 0
        ```

    * token：it's used for authentication with K8S's service account token
        before that you need create an user account at first.

        ```shell
        kubectl create serviceaccount gordenfl          
        ```

        then create the token for this user

        ```shell
        kubectl apply -f - <<EOF              
            apiVersion: v1
            kind: Secret
            metadata:
            name: gordenfl-token
            annotations:
                kubernetes.io/service-account.name: gordenfl
            type : kubernetes.io/service-account-token
        EOF
        ```

        after that, you can get the token with this command:

        ```shell
            kubectl get secret gordenfl-token -o jsonpath='{.data.token}'
        ```

        if you want to use it, you must base64 decode:

        ```shell
            kubectl get secret gordenfl-token -o jsonpath='{.data.token}'  # this is show the token 
            kubectl get secret gordenfl-token -o jsonpath='{.data.token}' | base64 --decode  # this is decode from base64
        ```

    * namespace：make sure the namespace for this program。

    * deployment：name of the deployment。

    * container：name of container。

    * image： name and label for the image。

4. ✅ Overview of the workflow of GitHub Actions

    * Trigger condition: When you push code to a specified branch (such as main) of a GitHub repository, GitHub Actions will be triggered.

    * Build a Docker image: In the Actions workflow, the Dockerfile is used to build the project's Docker image first.

    * Push the image to Docker Hub: After the build is complete, the image will be pushed to Docker Hub or other container image repositories.

    * Deploy to a Kubernetes cluster: Next, use the Kubernetes configuration file (such as the Deployment YAML file) to deploy the newly built image to the specified Kubernetes cluster.
    
    All of these operations are performed in the GitHub Actions runtime environment, usually on a cloud server provided by GitHub.

5. 🌐 Network access requirements
    It is important to note that the running environment of GitHub Actions requires access to the API server of your Kubernetes cluster. If your cluster is located in a private network, you may need to take additional measures, such as using a VPN, jump server, or secure tunnel to ensure that GitHub Actions can access the cluster securely.




