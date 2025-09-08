# Introduction 
Contexto 
Es importante conocer sobre los registros de nuestras instancias RDS de dev/qa/prod para solucionar los problemas. En lugar de pasar por la Consola AWS y hacer click se pefiere obtenerlo por mediante un script awslogs. 

# Prerequisitos
- Tener una base de datos RDS(terraform init && terraform plan && terraform apply)

# Ejecucion
`cd script && pip install -r requirements.txt && python main.py 2025-08-01 2025-08-29`

## fuente

[blog post](https://renehernandez.io/snippets/access-rds-logs-in-cloudwatch-using-awslogs/)