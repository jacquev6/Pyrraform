variable "uptimerobot_api_key" {
  type = string
}

provider "uptimerobot" {
  api_key = var.uptimerobot_api_key
}

provider "pyrraform-test" {}

data "pyrraform-test_answer" "answer" {
    foo = "bar"
}

output "foo" {
    value = data.pyrraform-test_answer.answer.foo
}

data "uptimerobot_account" "account" {}

output "email" {
    value = data.uptimerobot_account.account.email
}
