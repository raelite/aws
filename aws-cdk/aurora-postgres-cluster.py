"""
@Author: Raj Tilak Bhowmick
This CDK app creates an Aurora Postgres Cluster with secret getting generated from AWS Secrets Manager
with 30 day single user rotation. Some values such as VPC, Subnet-Group, etc are taken from existing environment
"""
from aws_cdk import core as cdk
from aws_cdk import core
from aws_cdk import aws_rds as _rds
from aws_cdk import aws_ec2 as _ec2


class AuroraPostgresCluster(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # EXISTING VALUES IN YOUR AWS ENVIRONMENT #

        vpc = _ec2.Vpc.from_lookup(
            self,
            id="DefaultVPC",
            vpc_id="REPLACE WITH YOUR EXISTING VPC-ID"
        )
        parameter_group = _rds.ParameterGroup.from_parameter_group_name(
            self,
            id="DefaultPG",
            parameter_group_name="REPLACE WITH YOUR EXISTING SECURITY GROUP-NAME"
        )
        security_group = _ec2.SecurityGroup.from_security_group_id(
            self,
            id="DefaultSG",
            security_group_id="REPLACE WITH YOUR EXISTING SECURITY GROUP-ID"
        )
        subnet_group = _rds.SubnetGroup.from_subnet_group_name(
            self,
            id="DefaultSubnetGrp",
            subnet_group_name="REPLACE WITH YOUR EXISTING SUBNET GROUP-NAME"
        )
        ###########################################

        cluster = _rds.DatabaseCluster(
            self,
            id="AuroraPostgresCluster",
            engine=_rds.DatabaseClusterEngine.aurora_postgres(
                version=_rds.AuroraPostgresEngineVersion.VER_12_4
            ),
            instance_props={
                "instance_type": _ec2.InstanceType.of(
                    _ec2.InstanceClass.BURSTABLE3,
                    _ec2.InstanceSize.MEDIUM
                ),
                "vpc_subnets": {
                    "subnet_type": _ec2.SubnetType.PUBLIC,
                },
                "publicly_accessible": True,
                "auto_minor_version_upgrade": True,
                "vpc": vpc,
                "parameter_group": parameter_group,
                "security_groups": [security_group]
            },
            instances=1,  # DEFAULT: 2 (WRITER & READER)
            port=3306,
            credentials=_rds.Credentials.from_generated_secret("adminroot"), # AUTOMATICALLY GENERATES SECRET IN SECRETS-MANAGER
            removal_policy=core.RemovalPolicy.DESTROY,
            parameter_group=parameter_group,
            subnet_group=subnet_group
        )
        cluster.add_rotation_single_user()  # ADDS SECRET ROTATION (DEFAULT: 30 DAYS)
