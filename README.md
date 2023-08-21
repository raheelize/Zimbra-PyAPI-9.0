Description: Zimbra 9.0 Python APIs for Account Management, Creation, Domain Registration, and Status Management

Introduction:
This repository contains a collection of Python scripts that provide APIs for managing Zimbra 9.0 accounts, domains, and related functionalities. The scripts allow you to interact with the Zimbra server's administration interface through SOAP requests, enabling tasks such as account creation, domain registration, status management, password resets, and more.

Features:

    Account Management: Create, activate, deactivate, and delete user accounts.
    Domain Management: Register, lock, and activate domains, and retrieve domain information.
    Password Management: Reset passwords for user accounts.
    Admin Delegation: Assign administrative delegation rights to specified users.
    Mailbox Quotas: Set mailbox quotas and limits for domains.
    Connection and Authentication: Authenticate with the Zimbra server using tokens and CSRF tokens.

Usage:

    Clone the repository to your local machine.
    Set up the required configuration parameters (HOST, PORT, USERNAME, PASSWORD) in the 'config.py' file.
    Utilize the provided functions in the 'zimbra_api.py' file to interact with the Zimbra server using the Zimbra SOAP APIs.
    Each function is documented to describe its purpose and usage.

Contributions:
Contributions to enhance functionality, improve code quality, and extend API capabilities are welcome. Please follow the standard guidelines for pull requests and ensure that the new code is well-documented.

Disclaimer:
This repository is not officially associated with the Zimbra project or organization. It's an independent effort to provide a convenient way to interact with Zimbra servers using Python.

Note:
Please exercise caution when using these scripts in a production environment. Always ensure proper testing and validation before performing any actions that may affect user accounts or domains.
