
# CypherMate





![Logo](https://raw.githubusercontent.com/Pyshios/CypherMate/main/CypherMateLogo.png)



Say hello to CypherMate, your go-to Slack bot for secure and effortless password sharing! Need to whip up a one-time link or encrypt crucial details before passing them along? CypherMate is here to help. With just a handful of clicks, secure password sharing is at your fingertips, safeguarding your data and simplifying your workflow. Embrace the ease and security CypherMate brings to your Slack chats.



#### CypherMate in action
![Logo](https://raw.githubusercontent.com/Pyshios/CypherMate/main/WorkingAndComands.gif)



CypherMate offers a suite of powerful features to enhance security and efficiency in your Slack chats:

- **Encrypt**: Securely encrypt passwords and sensitive information directly within Slack.
- **Decrypt**: Safely decrypt received information with a simple command.
- **Create Link with Encryption**: Generate one-time links for sharing encrypted data, ensuring that only the intended recipient can access it.
- **Create Link without Encryption**: Quickly share non-sensitive information through one-time links for convenience.

Powered by Python and the Slack Bolt framework, CypherMate leverages the robust [OneTimeSecret.com API](https://onetimesecret.com/) for maximum security and ease of use.

## Getting Started

Before you dive into using CypherMate, there are a few prerequisites you'll need to ensure are in place. These requirements are necessary to install and run CypherMate smoothly in your Slack workspace.

### Prerequisites

1. **Slack Workspace**: You need to have access to a Slack workspace where you have permissions to install apps. If you're not the workspace administrator, you may need to request permission or assistance from your admin to install and set up CypherMate.

2. **Python Environment**: CypherMate is built using Python, so you'll need to have Python 3.x installed on your server or local machine where you plan to run the bot. Alongside Python, ensure that `pip` (Python's package installer) is also installed to handle the installation of dependencies.


    - Docker and docker compose 



3. **Slack Bolt for Python**: The Slack Bolt framework simplifies the process of building Slack apps with Python. You'll be using this to interact with the Slack API effectively. Installation instructions will be provided in the Installation section.

4. **OneTimeSecret Account and API Key**: Since CypherMate utilizes the OneTimeSecret.com API for creating one-time links and handling encryption, you'll need to create an account on OneTimeSecret.com and generate an API key. This API key will be used in your environment variables to allow CypherMate to interact with OneTimeSecret services.

5. **Server or Hosting Environment**: Depending on your use case, you may want to run CypherMate on a server or hosting environment. This could be a cloud server (e.g., AWS, GCP, Azure), a dedicated server, or even a local machine, depending on the scale and accessibility requirements of your Slack workspace.

Once you've ensured these prerequisites are in place, you can proceed with the installation of CypherMate.

## Deployment

Deploying CypherMate is streamlined to ensure you can get your Slack bot up and running with minimal hassle. Follow these steps to deploy CypherMate:

1. **Clone the Repository**: Start by cloning the CypherMate repository to your local system or server. Open a terminal and run the following command:

```bash
git clone https://github.com/Pyshios/CypherMate.git
```


## Configuration

Before running CypherMate, you'll need to set up your environment variables. This involves creating a `.env` file based on the provided `.env.example` file. These environment variables are crucial for the bot's operation, as they contain sensitive information required for authentication and integration with the Slack API and OneTimeSecret API.

### Populating `.env` File

1. Copy the `.env.example` file to a new file named `.env` in the same directory.

2. Open the `.env` file with your favorite text editor and fill in the values for the environment variables:

    ```
    # .env file
    SLACK_BOT_TOKEN=your_slack_bot_token_here
    SLACK_APP_TOKEN=your_slack_app_token_here
    OTS_USERNAME=your_ots_username_here
    OTS_API_TOKEN=your_ots_api_token_here
    ENCRYPTION_KEY=your_encryption_key_here
    OTS_API_URL="https://onetimesecret.com/api/v1/share"
    OTS_BASE_URL="https://onetimesecret.com/secret/"
    ```

    - `SLACK_BOT_TOKEN` and `SLACK_APP_TOKEN` are tokens you'll receive from Slack when you create and configure your bot app.
    - `OTS_USERNAME` and `OTS_API_TOKEN` are your OneTimeSecret username and API token, respectively.
    - `ENCRYPTION_KEY` is a secret key you create for encrypting data before it's sent to OneTimeSecret.
    - `OTS_API_URL` and `OTS_BASE_URL` are the API endpoint and base URL for OneTimeSecret, and typically do not need to be changed.

Ensure that you replace `your_slack_bot_token_here`, `your_slack_app_token_here`, `your_ots_username_here`, `your_ots_api_token_here`, and `your_encryption_key_here` with your actual data.

### Running CypherMate with Docker Compose

With your `.env` file set up, you can easily run CypherMate using Docker Compose. This approach simplifies the deployment process and ensures that your bot runs in a consistent and isolated environment.

1. Ensure you have Docker and Docker Compose installed on your system. If not, refer to the [official Docker documentation](https://docs.docker.com/get-docker/) for installation instructions.


2. In your terminal or command prompt, navigate to the directory containing your `docker-compose.yml` file.

3. Run the following command to build and start the CypherMate bot:

    ```bash
    docker-compose up
    ```

    This command builds the Docker image for CypherMate and starts the bot in a Docker container. Docker Compose automatically reads your `.env` file and passes the environment variables to the container.

Your CypherMate bot should now be running and connected to your Slack workspace. You can interact with it using the commands described in the Usage section.

## Usage/Examples

```bash
/decrypt_me
```
```bash
/encrypt_me
```
```bash
/get_link
```
