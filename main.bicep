@description('Location for all resources')
param location string = 'southcentralus'

@description('Location for CosmosDB (not available in South Central US)')
param cosmosLocation string = 'centralus'

@description('Base name for all resources')
param baseName string = 'cloudresumetest001'

// Storage Account (required by Function App)
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'st${baseName}'
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
}

// CosmosDB Account
resource cosmosAccount 'Microsoft.DocumentDB/databaseAccounts@2023-04-15' = {
  name: 'cosmos-${baseName}'
  location: cosmosLocation
  kind: 'GlobalDocumentDB'
  properties: {
    databaseAccountOfferType: 'Standard'
    locations: [
      {
        locationName: cosmosLocation
        failoverPriority: 0
      }
    ]
    capabilities: [
      {
        name: 'EnableTable'
      }
      {
        name: 'EnableServerless'
      }
    ]
  }
}

// CosmosDB Table
resource cosmosTable 'Microsoft.DocumentDB/databaseAccounts/tables@2023-04-15' = {
  parent: cosmosAccount
  name: 'counter'
  properties: {
    resource: {
      id: 'counter'
    }
  }
}

// Function App
resource functionApp 'Microsoft.Web/sites@2023-01-01' = {
  name: 'func-${baseName}'
  location: location
  kind: 'functionapp,linux'
  properties: {
    siteConfig: {
      pythonVersion: '3.13'
      appSettings: [
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};EndpointSuffix=${environment().suffixes.storage};AccountKey=${storageAccount.listKeys().keys[0].value}'
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python'
        }
        {
          name: 'COSMOS_CONNECTION_STRING'
          value: cosmosAccount.listConnectionStrings().connectionStrings[0].connectionString
        }
      ]
    }
  }
}
