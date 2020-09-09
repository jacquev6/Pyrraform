variable "uptimerobot_api_key" {
  type = string
}

provider "uptimerobot" {
  api_key = var.uptimerobot_api_key
}

provider "pyrraform-test" {
    left_side = "love"
}

data "pyrraform-test_verse" "first" {
    right_side = "the answer"
}

output "first_verse" {
    value = data.pyrraform-test_verse.first.sentence
}

data "uptimerobot_account" "account" {}

output "email" {
    value = data.uptimerobot_account.account.email
}
