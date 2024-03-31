import os
import requests

from cryptography.fernet import Fernet
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Slack app credentials from environment variables
# SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")  # App-Level Token with the connections:write permission
# SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")  # Bot User OAuth Token

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
OTS_USERNAME = os.getenv("OTS_USERNAME")
OTS_API_TOKEN = os.getenv("OTS_API_TOKEN")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

# Get the encryption key from the environment variable
# ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

# Initialize the Slack app
# Initialize the Slack app
app = App(token=SLACK_BOT_TOKEN)

def share_secret(secret, ttl=3600, passphrase=None, recipient=None):
    """Stores a secret value using the One-Time Secret API."""
    url = "https://onetimesecret.com/api/v1/share"
    auth = (OTS_USERNAME, OTS_API_TOKEN)
    data = {'secret': secret, 'ttl': ttl, 'passphrase': passphrase, 'recipient': recipient}
    response = requests.post(url, data=data, auth=auth)
    response.raise_for_status()  # Verify successful request
    return response.json()

@app.command("/password_view")
def handle_password_command(ack, body, client, logger):
    """Opens the modal for entering password and optional passphrase/recipient."""
    ack()
    # Define the modal structure
    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "password_modal",
            "title": {"type": "plain_text", "text": "Encrypt & Share Password"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "close": {"type": "plain_text", "text": "Cancel"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "password_block",
                    "element": {"type": "plain_text_input", "action_id": "password_input"},
                    "label": {"type": "plain_text", "text": "Enter your text "}
                },
                {
                    "type": "section",
                    "block_id": "encryption_block",
                    "text": {"type": "mrkdwn", "text": "Do you want to encrypt the password?"},
                    "accessory": {
                        "type": "radio_buttons",
                        "options": [
                            {"text": {"type": "plain_text", "text": "Yes"}, "value": "yes"},
                            {"text": {"type": "plain_text", "text": "No"}, "value": "no"}
                        ],
                        "action_id": "encryption_choice"
                    }
                },
                {
                    "type": "input",
                    "block_id": "passphrase_block",
                    "element": {"type": "plain_text_input", "action_id": "passphrase_input"},
                    "label": {"type": "plain_text", "text": "Passphrase for the link (optional)"},
                    "optional": True
                },
                {
                    "type": "input",
                    "block_id": "recipient_block",
                    "element": {"type": "plain_text_input", "action_id": "recipient_input"},
                    "label": {"type": "plain_text", "text": "Recipient Email (optional)"},
                    "optional": True
                }
            ]
        }
    )

@app.view("password_modal")
def handle_modal_submission(ack, body, view, client, logger):
    """Handles modal submissions for creating one-time secrets."""
    ack()  # Acknowledge the view submission
    inputs = view["state"]["values"]
    password = inputs["password_block"]["password_input"]["value"]
    encrypt_choice = inputs["encryption_block"]["encryption_choice"]["selected_option"]["value"]
    passphrase = inputs.get("passphrase_block", {}).get("passphrase_input", {}).get("value")
    recipient = inputs.get("recipient_block", {}).get("recipient_input", {}).get("value")

    # Encrypt the password if requested
    if encrypt_choice == "yes":
        fernet = Fernet(ENCRYPTION_KEY.encode())
        password = fernet.encrypt(password.encode()).decode()

    # Share the password (encrypted or not) as a one-time secret
    try:
        secret_response = share_secret(secret=password, passphrase=passphrase, recipient=recipient)
        secret_link = f"https://onetimesecret.com/secret/{secret_response['secret_key']}"
        message = f"Here's your one-time link: {secret_link}"
    except Exception as e:
        logger.error(f"Error creating one-time link: {e}")
        message = "Failed to create one-time link. Please try again."

    client.chat_postEphemeral(channel=body["user"]["id"], user=body["user"]["id"], text=message)


@app.action("encryption_choice")
def handle_encryption_choice_action(ack, body, logger, client):
    ack()  # Acknowledge the action request immediately to avoid timeouts
    logger.info(body)  # Log the action request body for debugging

    # Extract necessary information from the action request
    user_id = body["user"]["id"]
    selected_option = body["actions"][0]["selected_option"]["value"]

    # Optional: Update internal state or respond to the user based on the selected option
    # This could involve updating a UI element, sending a message, or other actions
    if selected_option == "yes":
        # Perform actions or update UI if encryption is selected
        client.chat_postEphemeral(
            channel=user_id,
            user=user_id,
            text="You've selected to encrypt your password."
        )
    elif selected_option == "no":
        # Perform actions or update UI if encryption is not selected
        client.chat_postEphemeral(
            channel=user_id,
            user=user_id,
            text="You've chosen not to encrypt your password."
        )
# Handle the modal submission
def handle_modal_submission(ack, body, view, client, logger):
    """Handles the modal submission for password encryption and sharing."""
    ack()
    inputs = view["state"]["values"]
    password = inputs["password_block"]["password_input"]["value"]
    encrypt_choice = inputs["encryption_block"]["encryption_choice"]["selected_option"]["value"]
    passphrase = inputs.get("passphrase_block", {}).get("passphrase_input", {}).get("value")
    recipient = inputs.get("recipient_block", {}).get("recipient_input", {}).get("value")

    if encrypt_choice == "yes":
        fernet = Fernet(ENCRYPTION_KEY.encode())
        password = fernet.encrypt(password.encode()).decode()

    try:
        secret_response = share_secret(secret=password, passphrase=passphrase, recipient=recipient)
        secret_link = f"https://onetimesecret.com/secret/{secret_response['secret_key']}"
        message = f"Here's your one-time link: {secret_link}"
    except Exception as e:
        logger.error(f"Error creating one-time link: {e}")
        message = "Failed to create one-time link. Please try again."

    client.chat_postEphemeral(channel=body["user"]["id"], user=body["user"]["id"], text=message)


@app.command("/decrypt_password")
def open_decrypt_modal(ack, body, client):
    ack()

    # Modal JSON payload defining the structure of the modal
    modal = {
        "type": "modal",
        "callback_id": "decrypt_modal",
        "title": {"type": "plain_text", "text": "Decrypt Password"},
        "submit": {"type": "plain_text", "text": "Decrypt"},
        "blocks": [
            {
                "type": "input",
                "block_id": "encryption_block",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "encrypted_password_input",
                    "multiline": True
                },
                "label": {"type": "plain_text", "text": "Enter the encrypted password"}
            }
        ]
    }

    # Opening the modal
    client.views_open(trigger_id=body["trigger_id"], view=modal)


@app.view("decrypt_modal")
def handle_decrypt_submission(ack, body, view, client):
    ack()

    # Extract the submitted encrypted password
    encrypted_password = view["state"]["values"]["encryption_block"]["encrypted_password_input"]["value"]

    # Assuming ENCRYPTION_KEY is defined globally as before
    fernet = Fernet(ENCRYPTION_KEY.encode())

    # Decrypting the password
    try:
        decrypted_password = fernet.decrypt(encrypted_password.encode()).decode()

        # Sending the decrypted password to the user - consider a more secure method
        user_id = body["user"]["id"]
        client.chat_postEphemeral(
            channel=user_id,
            user=user_id,
            text=f"Your decrypted password is: {decrypted_password}"
        )
    except Exception as e:
        # Handle decryption failure (wrong key, corrupted input, etc.)
        client.chat_postEphemeral(
            channel=user_id,
            user=user_id,
            text="Failed to decrypt the password. Please ensure it's correctly encrypted."
        )


# Start the Slack app in Socket Mode
if __name__ == "__main__":
    if not SLACK_APP_TOKEN or not SLACK_BOT_TOKEN:
        print("SLACK_APP_TOKEN and SLACK_BOT_TOKEN environment variables not set")
        exit(1)

    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()