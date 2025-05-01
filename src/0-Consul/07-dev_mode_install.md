# Consul in Dev mode.

This page will show the steps taken to install Consul in dev mode.

These steps are taken from the [Deploy Consul on VMs](https://developer.hashicorp.com/consul/tutorials/get-started-vms/virtual-machine-gs-deploy) page.

For this document as we will be following the page instructions we will not add the full steps here, just the initial setup of the lab itself.

I will also point out some customizations to fit my needs.

## What we will do:

- Deploy your VM environment on AWS EC2 using Terraform
- Configure a Consul server
- Start a Consul server instance
- Configure your terminal to communicate with the Consul datacenter
- Bootstrap Consul ACL system and create tokens for Consul management
- Interact with Consul API, the KV store, and the UI

## Prerequisites

- An AWS account configured for use with Terraform
- aws-cli >= 2.0
- terraform >= 1.0
- git >= 2.0

## Clone the repository and change into the directory

```bash
$ git clone https://github.com/hashicorp-education/learn-consul-get-started-vms
$ cd learn-consul-get-started-vms
```

## Create the initial infrastructure

```bash
$ terraform init
$ terraform apply
```

## Change the region to fit your needs

The default region is `us-east-1`. You can change it to your preferred region by modifying the `aws_region` variable in the `variables.tf` file.

For me I will be using `eu-central-1` as my region.

```hcl
variable "aws_region" {
  description = "The AWS region to deploy the infrastructure in"
  type        = string
  default     = "eu-central-1"
}
```

I'm changing it here so I don't have to change it in every command line run or in each of the multiple tfvars on the repo.

## Notes on the lab and possible corrections:

- Typo on {Create server tokens}(https://developer.hashicorp.com/consul/tutorials/get-started-vms/virtual-machine-gs-deploy?variants=consul-workflow%3Aaws#create-server-tokens) section on the manual configuration. It says the following:
  > In this section, you manually create ACL tokens for the Consul DNS service and your server agent. Perform the following steps for each token:
  >
  > 1. Define the ACL riles in a policy configuration file.
- We should be having `rules` instead of `riles`.
