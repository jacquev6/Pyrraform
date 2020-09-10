provider "configured-datasource" {
    left_side = "love"
}

data "configured-datasource_verse" "first" {
    right_side = "the answer"
}

output "first_verse" {
    value = data.configured-datasource_verse.first.sentence
}
