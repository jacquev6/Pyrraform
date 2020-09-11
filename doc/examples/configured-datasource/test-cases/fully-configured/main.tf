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

    datasource_block_list {
        block_attribute = "list 1"
    }
    datasource_block_list {
        block_attribute = "list 2"
    }
    # Block repeated on purpose to explore the difference between list and set
    datasource_block_list {
        block_attribute = "list 2"
    }

    datasource_block_set {
        block_attribute = "set 1"
    }
    datasource_block_set {
        block_attribute = "set 2"
    }
    # Block repeated on purpose to explore the difference between list and set
    datasource_block_set {
        block_attribute = "set 2"
    }

    # Labels can be quoted
    datasource_block_map "a" {
        block_attribute = "map 1"
    }
    # Labels can be unquoted
    datasource_block_map b {
        block_attribute = "map 2"
    }
}

output "provider_config" {
    value = data.configured-datasource_dump-configs.configs.provider
}

output "datasource_config" {
    value = data.configured-datasource_dump-configs.configs.datasource
}
