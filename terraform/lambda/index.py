import boto3
def lambda_handler(event, context):

    eks = boto3.client('eks')
    region_name = "us-east-1"

    cluster_name = "my-multi-nodegroup-cluster"

    nodegroup_names = ['general-purpose-ng', 'high-cpu-ng']
    new_desiredSize = 0
    new_minSize = 0
    new_maxSize = 1

    # Loop through the node groups and update their desired capacity to 0
    for nodegroup_name in nodegroup_names:
        response = eks.update_nodegroup_config(
            clusterName=cluster_name,
            nodegroupName=nodegroup_name,
            scalingConfig={
                "desiredSize": new_desiredSize,
                "minSize": new_minSize,
                "maxSize": new_maxSize
            }
        )

        # Print the response
        print(response)
    # cluster_name = "my-multi-nodegroup-cluster"

    # nodegroup_sizes = {
    #     'general-purpose-ng': 2,
    #     'high-cpu-ng': 1
    # }

    # nodegroup_minsizes = {
    #     'general-purpose-ng': 1,
    #     'high-cpu-ng': 1
    # }

    # nodegroup_maxsizes = {
    #     'general-purpose-ng': 2,
    #     'high-cpu-ng': 2
    # }

    # for nodegroup_name, max_size in nodegroup_maxsizes.items():
    #     response = eks.describe_nodegroup(
    #         clusterName=cluster_name,
    #         nodegroupName=nodegroup_name
    #     )
    #     current_size = response['nodegroup']['scalingConfig']['maxSize']

    #     if max_size != current_size:
    #         response = eks.update_nodegroup_config(
    #             clusterName=cluster_name,
    #             nodegroupName=nodegroup_name,
    #             scalingConfig={
    #                 'maxSize': max_size
    #             }
    #         )
    #         print(
    #             f"Updated maximum size for node group {nodegroup_name} to {max_size}")
    #     else:
    #         print(
    #             f"Maximum size is already {max_size} for node group {nodegroup_name}")

    # for nodegroup_name, desired_size in nodegroup_sizes.items():
    #     response = eks.describe_nodegroup(
    #         clusterName=cluster_name,
    #         nodegroupName=nodegroup_name
    #     )
    #     current_size = response['nodegroup']['scalingConfig']['desiredSize']

    #     if desired_size != current_size:
    #         response = eks.update_nodegroup_config(
    #             clusterName=cluster_name,
    #             nodegroupName=nodegroup_name,
    #             scalingConfig={
    #                 'desiredSize': desired_size
    #             }
    #         )
    #         print(
    #             f"Updated desired size for node group {nodegroup_name} to {desired_size}")
    #     else:
    #         print(
    #             f"Desired size is already {desired_size} for node group {nodegroup_name}")

    # for nodegroup_name, min_size in nodegroup_minsizes.items():
    #     response = eks.describe_nodegroup(
    #         clusterName=cluster_name,
    #         nodegroupName=nodegroup_name
    #     )
    #     current_size = response['nodegroup']['scalingConfig']['minSize']

    #     if min_size != current_size:
    #         response = eks.update_nodegroup_config(
    #             clusterName=cluster_name,
    #             nodegroupName=nodegroup_name,
    #             scalingConfig={
    #                 'minSize': min_size
    #             }
    #         )
    #         print(
    #             f"Updated minimal size for node group {nodegroup_name} to {min_size}")
    #     else:
    #         print(
    #             f"Minimal size is already {min_size} for node group {nodegroup_name}")