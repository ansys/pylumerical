.. _ref_interop_server:

Interop server
==============

With Lumerical 2023 R1.2 and later, it is possible to use the Python API remotely. This documentation will show how to run the interop server required to use the remote API.

.. note::
    The interop server is available on Linux only. 

Three shell scripts are provided, located in `[path to Lumerical]/api/interop-server/scripts/linux`

* generate_certificate.sh
* interop_server_start.sh
* interop_server_stop.sh

Interop server security
------------------------

Connecting clients to the interop server are not authenticated, and remote API commands from the connecting client will have the same permissions as the user that started the interop server process on the host. 
This could expose the host’s local user space to the remote operator.

To mitigate potential security risks, the following precautions should be taken when setting up the interop server:

1. The interop server should only be deployed on a restricted internal network.
2. When possible, the interop server should be deployed in a container. Instructions on building the container using the Dockerfile provided in the installation package can be found in the `Dockerfile Knowledge Base article <https://optics.ansys.com/hc/en-us/articles/12325704816659-Dockerfile-support>`__.
3. If deployment in a container is not possible, a restricted user or user group should be used when starting the interop server to avoid impacting existing users. The interop server should not be run as a user with sudo or root permissions.

Generate certificates
----------------------

The interop server requires a certificate to encrypt the communication between the client and the server. 
You can use your own certificate, or use the script generate_certificate.sh to generate them and place them in the user’s home folder, in `$HOME/.config/Lumerical/interop_server_certs/`

To run the script, move to the folder and run generate_certificate.sh. For example, if Lumerical 2023 R1.2 is installed in the default location:

.. code-block:: bash 

    cd /opt/Lumerical/v231/api/interop-server/script/linux
    ./generate_certificate.sh

Start and stop the interop server
---------------------------------

To start the interop server, run interop_server_start.sh from the same folder.

.. code-block:: bash

    ./interop_server_start.sh

The server accepts the following options:

1. interface IP address [default is 127.0.0.1]
2. port [default is 8989]
3. Path to server's key
4. Path to server’s certificate

Note the parameters have to be specified in that order. For example, if you want to specify the server’s key, you have to specify the previous ones as well (IP address and port).

The interop server should be able to receive incoming connection on the specified port. You may want to open the port or disable the firewall on the machine. Please refer to your Linux distribution documentation. 
You will need to open a range of ports above the starting port in order to handle multiple connections. We suggest the starting port plus a range of at least 5.

To stop the server, run (from the same folder):

.. code-block:: bash

    ./interop_server_stop.sh