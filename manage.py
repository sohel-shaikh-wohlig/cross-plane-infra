import os
import yaml
from kubernetes import client, config, dynamic
from kubernetes.client import api_client

files = 'http.proxy/mock-io.yaml'.split(",")
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

            # Create Record in Cloudflare
            client = dynamic.DynamicClient(api_client.ApiClient(
                configuration=config.load_kube_config(config_file='./http.proxy/kubeconfig.yaml')))
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
