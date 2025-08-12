1. Revisar los triggers: Verifica qué eventos activan la ejecución de la pipeline (por ejemplo, push a ciertas ramas, pull request, etc.).

```

trigger:

branches:

include:

- refs/heads/dev

```

2. Identificar variables necesarias en cada ambiente: Toma nota de las variables que necesitarás usar en los diferentes stages (como development, production, etc.). Algunas dependerán del tipo de trigger.

```

variables:

- name: helmRepositoryName

value: 'cd-ecr-qa-dotnet-helm'

  

- name: ecrHelmCredentials

value: 'aws-ecr-credentials-qa'

# DEVELOPMENT

- name: acrAwsCredentials

value: 'aws-ecr-credentials'

.... more

- name: RepositoryName

value: 'cd-ecr-dev-cluster'

```

3. Definir y reutilizar el template: Crea un archivo template que contenga configuraciones comunes. Asígnale un alias o nombre identificador para poder reutilizarlo fácilmente en otros stages.

```

resources:

repositories:

- repository: template

name: "dsec/pipeline-template"

```

4. Declarar variables del template en el stage de Build: Incluye las variables del template (creado en el paso anterior) dentro del stage de Build, especialmente para los jobs de docker y build.

```

stages:

- stage: Build

variables:

- group: xyz-desk-order-fulfillment-dev

jobs:

- job: Compile

variables:

buildConfiguration: "Release"

# POR EJEMPLO: https://dev.azure.com/xyz/dsec/_git/pipeline-template?path=/templates/dotnet-build.yaml

# - task: DotNetCoreCLI@2

# displayName: 'Build'

# inputs:

# arguments: '--configuration $(buildConfiguration)'

# projects: '${{parameters.ApiDirectory}}/*.csproj'/

steps:

- template: "templates/dotnet-build.yaml@template"

```

5. Activar el stage de development: Solo se ejecute cuando se hagan cambios en la rama dev (refs/heads/dev) y no se pueda ejecutar manualmente.

```

- stage: DeployDEV

condition: and(succeeded(), and( eq(variables['Build.SourceBranch'], 'refs/heads/dev'), ne(variables['Build.Reason'],'Manual')))

.....

```

5.1. Variables de DeployDEV desde las Library Variables: Usa variables centralizadas definidas en la sección de Libraries de Azure DevOps para el stage DeployDEV.

```

variables:

- group: xyz-desk-order-fulfillment-dev

- group: xyz-desk-order-fulfillment-dev-secret

```

5.2. Variables desde env-data.yaml: Extrae variables del archivo env-data.yaml para usarlas en este stage. Este archivo puede contener configuraciones por ambiente.

```

variables:

..... more code

- name: tmpPath

value: 'tmp/env-data-$(APPLICATION_NAME).yaml'

# - task: Bash@3 ## https://dev.azure.com/xyz/dsec/_git/pipeline-template?path=/templates/deployment-gitops.yaml&version=GBmain&line=62&lineEnd=62&lineStartColumn=11&lineEndColumn=15&lineStyle=plain&_a=contents

# displayName: 'Copy variables if exist'

```

5.3. Variables para GitOps Development(gitops-development): Copia las variables necesarias desde env-data.yaml al gitops-development(configma[s y secrets]).

```

- name: scriptPath

value: './gitops/utils/scripts/argocd-automation.sh'

# - task: Bash@3 ## https://dev.azure.com/xyz/dsec/_git/gitops?path=/utils/templates/values.yaml

# displayName: 'Execute bash of argoCD'

```

5.4. Pasar variables al template de deployment: Asegúrate de pasar correctamente las variables al template que maneja el despliegue (deployment), para que todo funcione de manera dinámica y reusable.

```

jobs:

- job: deploy_with_argocd

displayName: 'Deploy with ArgoCD'

steps:

- template: 'templates/deployment-gitops.yaml@template'

```