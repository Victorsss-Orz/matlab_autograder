When you are developing the grader or workspace image for the first time:

- Create an account on Docker Hub (ignore if there is already a CS101 account)
- Make sure you have Docker installed (you probably already do since you are using PrairieLearn locally)
- Log in to Docker Hub in your terminal, instructions here: https://docs.docker.com/reference/cli/docker/login/

Make whatever change you want to the Dockerfile / install scripts, and then:

- Navigate to where the Dockerfile is in your terminal
- Run `docker build -t [DOCKER ACCOUNT NAME HERE]/[IMAGE NAME HERE]:[TAG HERE] .` (for example, `docker build -t uiuccs101/octave-autograder:latest .`) More info here: https://docs.docker.com/reference/cli/docker/buildx/build/
- Push the built image to Docker Hub using `docker push [DOCKER ACCOUNT NAME HERE]/[IMAGE NAME HERE]:[TAG HERE]`. More info here: https://docs.docker.com/reference/cli/docker/image/push/
- If you are using a different tag (`latest` is used by default) what the question was already using, make sure to change it in `info.json`. Then test the new image locally
- When you are happy with the image, go to the "Sync" page for the course in PrairieLearn and click "Sync all images from Docker Hub to PrairieLearn"
