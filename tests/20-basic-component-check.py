#!/usr/bin/python3

import amulet
import os
import unittest
import yaml

SECONDS_TO_WAIT = 1800


def find_bundle():
    '''Locate the bundle to load for this test.'''
    bundle = os.getenv('BUNDLE')
    if not bundle:
        bundle = os.path.join(os.path.dirname(__file__), '..', 'bundle.yaml')
    return bundle


class IntegrationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.deployment = amulet.Deployment(series='xenial')
        cls.bundle_file = find_bundle()
        with open(cls.bundle_file) as stream:
            bundle_yaml = stream.read()
        bundle = yaml.safe_load(bundle_yaml)
        cls.deployment.load(bundle)

        # Allow some time for Juju to provision and deploy the bundle.
        cls.deployment.setup(timeout=SECONDS_TO_WAIT)

        # Wait for the system to settle down.
        application_messages = {'kubernetes-worker':
                                'Kubernetes worker running.'}
        cls.deployment.sentry.wait_for_messages(application_messages,
                                                timeout=600)

        cls.easyrsas = cls.deployment.sentry['easyrsa']
        cls.etcds = cls.deployment.sentry['etcd']
        cls.flannels = cls.deployment.sentry['flannel']
        cls.masters = cls.deployment.sentry['kubernetes-master']
        cls.workers = cls.deployment.sentry['kubernetes-worker']
        cls.e2e = cls.deployment.sentry['kubernetes-e2e']

    def test_cluster_info(self):
        '''Test that kubectl is installed and the cluster appears healthy.'''
        for master in self.masters:
            info = 'kubectl --kubeconfig /home/ubuntu/kube/config cluster-info'
            print(info)
            output, rc = master.run(info)
            print(output)
            self.assertTrue(rc == 0)
            self.assertTrue('Kubernetes master^[[0m is running' in output)
            self.assertTrue('KubeDNS^[[0m is running' in output)


if __name__ == '__main__':
    unittest.main()
