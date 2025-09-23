# Introduction 
## install 

```
curl -s https://raw.githubusercontent.com/terraform-linters/tflint/master/install_linux.sh | bash
```

## execute

```
## tflint --init # optional without precomit
## tflint # optional without precomit
pre-commit run -a
```

## as rules

```
https://github.com/terraform-linters/tflint-ruleset-aws/blob/v0.41.0/docs/rules/README.md#best-practicesnaming-conventions
```