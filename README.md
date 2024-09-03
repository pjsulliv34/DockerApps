### Heroku Implementation

1. **Create and Test Docker Image**
   - Build the Docker image:
     ```bash
     docker build -t {image name} .
     ```
   - Test the Docker image by running a container locally:
     ```bash
     docker run -d -p {port}:{port} {image name}
     ```
   - Verify that the image is running correctly.

2. **Deploy to Heroku**
   - **Create a Heroku app:**
     - Log in to Heroku:
       ```bash
       heroku login
       ```
     - Create a new Heroku app:
       ```bash
       heroku create --stack {app name}
       ```
   - **Prepare your app for Heroku:**
     - Create a `heroku.yml` file.
     - Comment out the `CMD` statement and `EXPOSE` port in the Dockerfile.
   - **Initialize Git and Deploy:**
     - Initialize an empty Git repository:
       ```bash
       git init
       ```
     - Add the repository to Git:
       ```bash
       git add .
       git commit -am "message"
       ```
     - Deploy the app to Heroku:
       ```bash
       git push heroku master
       ```

3. **If the App is Not a Container**
   - Use the following command to set the Heroku stack to container:
     ```bash
     heroku stack:set container
     ```
