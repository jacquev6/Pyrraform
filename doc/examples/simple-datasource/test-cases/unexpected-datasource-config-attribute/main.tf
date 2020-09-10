provider "simple-datasource" {}

data "simple-datasource_answer" "answer" {
    unexpected = 42
}

output "answer" {
    value = data.simple-datasource_answer.answer.value
}
