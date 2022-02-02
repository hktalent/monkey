from typing import List

from infection_monkey.credential_collectors.credentials.credentials import Credentials
from infection_monkey.credential_collectors.i_collector import ICollector
from infection_monkey.system_info.windows_cred_collector import pypykatz_handler
from infection_monkey.system_info.windows_cred_collector.windows_credentials import (
    WindowsCredentials,
)


class MimikatzCredentialCollector(ICollector):
    @staticmethod
    def collect():
        creds = pypykatz_handler.get_windows_creds()
        return MimikatzCredentialCollector.cred_list_to_cred_dict(creds)

    @staticmethod
    def cred_list_to_cred_dict(creds: List[WindowsCredentials]) -> Credentials:
        cred_dict = {}
        for cred in creds:
            # TODO: This should be handled by the island, not the agent. There is already similar
            #       code in monkey_island/cc/models/report/report_dal.py.
            # Lets not use "." and "$" in keys, because it will confuse mongo.
            # Ideally we should refactor island not to use a dict and simply parse credential list.
            key = cred.username.replace(".", ",").replace("$", "")
            cred_dict.update({key: cred.to_dict()})
        creds = Credentials(type="Mimikatz", data=cred_dict)
        return creds
