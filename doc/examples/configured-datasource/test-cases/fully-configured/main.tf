provider "configured-datasource" {
    provider_attribute_number = 42
    provider_attribute_string = "forty-two"
    provider_attribute_boolean = true
}

data "configured-datasource_dump-configs" "configs" {
    datasource_attribute_number = 57
    datasource_attribute_string = "fifty-seven"
    datasource_attribute_boolean = false

    datasource_attribute_string_required = "here it is"

    datasource_attribute_number_list = [43, 44, 45]
    datasource_attribute_string_list_list = [["a", "b"], [], ["c", "d", "e"]]

    datasource_attribute_object = {
        a = 46
    }

    datasource_block_single_optional {
        block_attribute = "foo 3"
    }

    datasource_block_single_required {
        block_attribute = "required"
    }
}

output "provider_config" {
    value = data.configured-datasource_dump-configs.configs.provider
}

output "datasource_config" {
    value = data.configured-datasource_dump-configs.configs.datasource
}
