

import azure.batch.batch_service_client as batch
import azure.batch.batch_auth as batchauth
import azure.batch.models as batchmodels

creds = batchauth.SharedKeyCredentials('searchtesting', 'F9TaLHOShNOskte7D/FUYcjvmLyv0tHWZmisokT73t8d6GNNNezhK/G//8mpX/Yb4ibqA7GL5r1AryDQoYW9dA==')
#config = batch.BatchServiceClientConfiguration(creds, base_url = 'https://searchtesting.centralus.batch.azure.com')
client = batch.BatchServiceClient(creds,batch_url='https://searchtesting.centralus.batch.azure.com')

image_ref_to_use = batch.models.ImageReference(
        publisher='microsoft-azure-batch',
        offer='ubuntu-server-container',
        sku='16-04-lts',
        version='latest')

# Specify a container registry
container_registry = batch.models.ContainerRegistry(
        user_name="jscholtes",
        password="dockerPa$$21")

# Create container configuration, prefetching Docker images from the container registry
container_conf = batch.models.ContainerConfiguration(
        container_image_names = ["jscholtes/pid_param_tune:latest"],
        container_registries =[container_registry])

new_pool = batch.models.PoolAddParameter(
            id="paramTune",
            display_name = "param_tune",
            virtual_machine_configuration=batch.models.VirtualMachineConfiguration(
                image_reference=image_ref_to_use,
                container_configuration=container_conf,
                node_agent_sku_id='batch.node.ubuntu 16.04'),
            vm_size='STANDARD_D1_V2',
            target_dedicated_nodes=3,
            target_low_priority_nodes=3)

client.pool.add(new_pool)