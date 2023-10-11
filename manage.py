import os
import yaml
from kubernetes import client, config, dynamic
from kubernetes.client import api_client

files = 'http.proxy/config-api-kings.yaml'.split(",")
print(files)

for f in files:
    # file = open(f, 'r')
    # print(file.read())
    # file.close()

    with open(f, 'r') as stream:
        try:
            content = yaml.safe_load(stream)
            fqdn = content["spec"]["virtualhost"]["fqdn"]
            proxied = True

            # Create a Python dictionary for Cloudflare YAML file
            cloudflare_data = {
                "apiVersion": "dns.cloudflare.crossplane.io/v1alpha1",
                "kind": "Record",
                "metadata": {
                    "name": fqdn
                },
                "spec": {
                    "forProvider": {
                        "zoneSelector": {
                            "matchLabels": {
                                "identifier": "dns-record"
                            }
                        },
                        "name": fqdn,
                        "content": "nlb.zodexchange.co.",
                        "proxied": proxied,
                        "type": "CNAME",
                        "zone": "7ea9fe1045447b31a338fbae6a1cfce9"
                    },
                    "providerConfigRef": {
                        "name": "zodexchange.co"
                    }
                }
            }

            ymal_string = yaml.dump(cloudflare_data)

            with open("./http.proxy/cloudflare.yaml", "w") as fileToWrite:
                fileToWrite.write(ymal_string)

            # with open("./http.proxy/kubeconfig.yaml") as f:
            #   kubeconfig = json.load(f)
            #   print(kubeconfig)
            #   config.load_kube_config_from_dictionary(kubeconfig)

            # config.load_kube_config(config_file='./http.proxy/kubeconfig.yaml')

            # v1 = client.CoreV1Api()
            # count = 10
            # w = watch.Watch()
            # for event in w.stream(v1.list_namespace, timeout_seconds=10):
            #    print("Event: %s %s" %
            #          (event['type'], event['object'].metadata.name))
            #    count -= 1
            #    if not count:
            #        w.stop()
            # print("Finished namespace stream.")

            # k8s_client = client.ApiClient()
            # utils.create_from_yaml(
            #    k8s_client, './http.proxy/cloudflare.yaml', verbose=True)

            # Connecting to Remote cluster

            # Define the bearer token we are going to use to authenticate.
            # See here to create the token:
            # https://kubernetes.io/docs/tasks/access-application-cluster/access-cluster/
            # aToken = "eyJhbGciOiJSUzI1NiIsImtpZCI6Img1c21hOF9HQW96SGlzY1lydldfeDFGaWdKZVh1ZlVCa1MxZkYzTDVWY0kifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4iLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjcxYmJjMTRmLTFkMmUtNGQ4Ni05ZmE5LTg3NGY1MzZkMGEwNiIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.LiLVTxuF-M5q9wPfb3s_EP9kAOV9z5NZHmSrEXmPpCV5IcpTiCYSn5FXISraGlzKMBHkTWMPWGY81umXtLpUociYhUEE02spfAfUZvvSnvTD95sLRHzXrIJsA_FoDCSA-ENknpXJ648qKVrNmT6VbblbXCugvptIQX0nwODkI8M3ggGc8sEq2-s5uVbDLNmq1_os_8jdHd7kpH0CQI9WVKS4Rw2ZlS0f7-6yuMnyGDGvWg2_G8k93o9zkWyczgll2n2KJVgxLa2DOUxiqRr2BT7LD4ithvwNgEoELGvZPt7ZU69Ra8sb0ko7SqoZ83tvCl1Waxd6MpsP81E3ZWFfCQ"
#
            # Create a configuration object
            # aConfiguration = client.Configuration()
#
            # Specify the endpoint of your Kube cluster
            # aConfiguration.host = "https://6A03AB76F7BBE7741AB0D061275815CF.gr7.us-east-1.eks.amazonaws.com:443"
#
            # aConfiguration.verify_ssl = True
#
            # aConfiguration.ssl_ca_cert = './http.proxy/ca.crt'
#
            # aConfiguration.api_key = {"authorization": "Bearer " + aToken}
#
            # Create a ApiClient with our config
            # aApiClient = client.ApiClient(aConfiguration)
#
            # Do calls
            # v1 = client.CoreV1Api(aApiClient)
            # print("Listing pods with their IPs:")
            # ret = v1.list_pod_for_all_namespaces(watch=False)
            # for i in ret.items:
            #    print(
            #        f"{i.status.pod_ip}\t{i.metadata.namespace}\t{i.metadata.name}")

            # Create Record in Cloudflare
            client = dynamic.DynamicClient(api_client.ApiClient(
                configuration=config.load_kube_config(config_file='./http.proxy/configuration.yaml')))
            api = client.resources.get(
                api_version="dns.cloudflare.crossplane.io/v1alpha1", kind="Record")
            name = fqdn
            record_manifest = {
                "apiVersion": "dns.cloudflare.crossplane.io/v1alpha1",
                "kind": "Record",
                "metadata": {
                    "name": fqdn
                },
                "spec": {
                    "forProvider": {
                        "content": "nlb.zodexchange.co.",
                        "name": fqdn,
                        "proxied": proxied,
                        "type": "CNAME",
                        "zone": "7ea9fe1045447b31a338fbae6a1cfce9",
                        "zoneSelector": {
                            "matchLabels": {
                                "identifier": "dns-record"
                            }
                        }
                    },
                    "providerConfigRef": {
                        "name": "zodexchange.co"
                    }
                }
            }
            record = api.create(body=record_manifest, namespace='default')
            record_created = api.get(name=name, namespace="default")

            # Delete Record on Cloudflare
            # client = dynamic.DynamicClient(api_client.ApiClient(
            #    configuration=config.load_kube_config(config_file='./http.proxy/kubeconfig.yaml')))
            # api = client.resources.get(
            #    api_version="dns.cloudflare.crossplane.io/v1alpha1", kind="Record")
            # api.delete("rates.playexch.io")

        except yaml.YAMLError as exc:
            print(exc)
