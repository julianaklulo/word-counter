resource "aws_security_group" "database" {
  name        = "Database security group"
  description = "Security group for database"
  vpc_id      = module.vpc.vpc_id

  ingress {
    description = "Database security group VPC"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = module.vpc.private_subnets_cidr_blocks
  }

  egress {
    description = "Database security group VPC"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_subnet_group" "dbsg" {
  name       = "database-subnet-group-dbsg"
  subnet_ids = module.vpc.private_subnets
}

resource "aws_db_instance" "default" {
  allocated_storage      = 10
  engine                 = "postgres"
  instance_class         = "db.t3.small"
  db_subnet_group_name   = aws_db_subnet_group.dbsg.name
  vpc_security_group_ids = [aws_security_group.database.id]
  storage_encrypted      = true
  name                   = "mydatabase"
  username               = var.database_username
  password               = var.database_password
}