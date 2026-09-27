## Thank you so much for yourt time 

## Problem 

duplicating iac code makes it dificult to maintin and keep consistent.

## Solution

having a reusable terraform module for  any kind of resource. we can use the same module for dev, qa, prod environment  without rewriting code.  to keep the proyect simple with modules  and maintainable in the futurer we can add ci pipeline  everytime someone opens a PR  the pipeline runs to cehck the code formating

```
terraform format
```
 which checks the code formating

```
terraform  validate
```

which checks that the terrfaorm code is valid . This help us with  to find mistakes  early and keep the module conssitent acrros the teams.
