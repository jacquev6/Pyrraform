provider "configured-datasource" {
}

data "configured-datasource_dump-configs" "configs" {
    datasource_attribute_string_required = "here it is"
    datasource_block_single_required {
        block_attribute = "required"
    }

    datasource_block_map a {
        block_attribute = "map 1"
    }
    datasource_block_map a {
        block_attribute = "map 2"
    }
}

output "provider_config" {
    value = data.configured-datasource_dump-configs.configs.provider
}

output "datasource_config" {
    value = data.configured-datasource_dump-configs.configs.datasource
}
