provider "configured-datasource" {}

data "configured-datasource_dump-configs" "configs" {
    datasource_attribute_string_required = "here it is"

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
