provider "simple-datasource" {
    unexpected = 42
}

data "simple-datasource_answer" "answer" {}

output "answer" {
    value = data.simple-datasource_answer.answer.value
}
