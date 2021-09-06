"""
@AUTHOR: Raj Tilak Bhowmick
@DATE: 07-09-2021
This Boto3 script registers a RDS cluster or instance as scalable target and then applies Target-Tracking-Scaling-Policy.
This can be modified to support other supported services.
"""
import boto3


def execute():
    try:
        session = boto3.session.Session(profile_name='YOUR-NAMED-PROFILE ', region_name='YOUR-TARGET-REGION')

        registerScalableTarget()
        putScalingPolicy()

    except Exception as e:
        print("Exception Raised :: execute() ::" + str(e))


def registerScalableTarget():
    try:
        session = boto3.session.Session(profile_name='YOUR-NAMED-PROFILE', region_name='YOUR-TARGET-REGION')

        autoscaling_client = session.client('application-autoscaling')

        response = autoscaling_client.register_scalable_target(
            ServiceNamespace='rds',
            ResourceId='cluster:YOUR-CLUSTER-NAME',
            ScalableDimension='rds:cluster:ReadReplicaCount',
            MinCapacity=0,
            MaxCapacity=3,
        )
    except Exception as e:
        print("Exception Raised :: registerScalableTarget() ::" + str(e))


def putScalingPolicy():
    try:
        session = boto3.session.Session(profile_name='YOUR-NAMED-AWS-PROFILE', region_name='TARGET-REGION')

        autoscaling_client = session.client('application-autoscaling')

        response = autoscaling_client.register_scalable_target(
            PolicyName='YOUR-POLICY-NAME',
            ServiceNamespace='rds',
            # ResourceId='',
            ScalableDimension='rds:cluster:ReadReplicaCount',
            PolicyType='TargetTrackingScaling',
            TargetTrackingScalingPolicyConfiguration={
                'TargetValue': 70.0,
                'PredefinedMetricSpecification': {
                    'PredefinedMetricType': 'RDSReaderAverageCPUUtilization',  # RDSReaderAverageDatabaseConnections
                },
                'ScaleOutCooldown': 600,
                'ScaleInCooldown': 300,
                'DisableScaleIn': False
            }
        )
    except Exception as e:
        print("Exception Raised :: putScalingPolicy() ::" + str(e))


execute()
