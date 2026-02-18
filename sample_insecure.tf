provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example" {
  name     = "rg-guardian-demo"
  location = "East US"
}

resource "azurerm_storage_account" "example" {
  name                     = "guardianstorage123"
  resource_group_name      = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  # No HTTPS enforcement
  enable_https_traffic_only = false
}

resource "azurerm_app_service_plan" "example" {
  name                = "guardian-appservice-plan"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  sku {
    tier = "Basic"
    size = "B1"
  }
}

resource "azurerm_app_service" "example" {
  name                = "guardian-appservice"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  app_service_plan_id = azurerm_app_service_plan.example.id

  site_config {
    ftps_state = "AllAllowed"
  }

  https_only = false
}
