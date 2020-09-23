provider "simple-datasource" {}

data "simple-datasource_answer" "answer" {}

output "answer" {
    value = data.simple-datasource_answer.answer.value
}
