#!/bin/bash

# Define the version of Terraform to install
TERRAFORM_VERSION="1.6.1"

# Download the Terraform binary
echo "\n📦 Downloading the terraform binary..."
curl -LO "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip"

# Unzip the downloaded file
echo "\n📂 Unzip the downloaded file..."
unzip "terraform_${TERRAFORM_VERSION}_linux_amd64.zip"

# Move the Terraform binary to /usr/local/bin
echo "\n☑️ Add Terraform to /usr/local/bin/ ..."
sudo mv terraform /usr/local/bin/

# Set the executable permissions
echo "\n✅ Change terraform binary to an executable..."
sudo chmod +x /usr/local/bin/terraform

# Clean up the downloaded zip file
echo "\n🧹 Clean up downloaded package..."
rm "terraform_${TERRAFORM_VERSION}_linux_amd64.zip"

# Verify the installation
echo "\n✅ Verify Terraform installation...\nInstalled Terraform version: "
terraform version