provider "pyrraform-test" {}

data "pyrraform-test_answer" "answer" {
    foo = "bar"
}

output "foo" {
    value = data.pyrraform-test_answer.answer.foo
}
