## Greetings!!!! Thank you so much for your time
## Problem
the main problem before implementing Ci/cD is the chaos manual process. which causese humand mistakes
## Solution
implement cd/cd with this developers manually built and deployed applications. Developer push code to git ci atomatically runs tests. The aplication is built into a deployable articfact/container. CD automatically deploy successful builds to any environment.

Let's look at an example.

to automate the deployment of a python app i am using gactions. i have to important job one is build where i check  the format with linter  then it runs the test cases  to make sure the application works. If something fails  the pipeline stop 

The second job is buidl and push  we need to give a tag version to the app image so we know which version we will release. we also securely log in in docker hub . finally it push  the docker image and then push .

