# Vital Records Printing #

Search for and print **Birth**, **Death**, and **Marriage** certificates.

Authors:
- Jonathan Yu
- Vincent Wong
- Panagis Alisandratos

## Development Environment Setup ##

1. Make sure you have VirtualBox version **5.1.18**.
    - If you have a later version and initial setup fails, please install 5.1.18 and retry.
    - You can upgrade to the latest version and `vagrant reload` after your setup is complete.

2. Copy `/ Development Tools / Vagrant Boxes /`**`rhel-6.8.virtualbox.box`** from 
`smb://csc.nycnet/doris/doris_share/development` into your project root or any desired directory.
    - You may need to supply your CSC credentials.

3. Run `./setup.sh` from within your project root directory.

    - This script will attempt to:
    
        - Add the *rhel-6.8-5.1.18* vagrant box
        - Install the vagrant plugins *vagrant-reload*, *vagrant-vbguest*, and *vagrant-triggers*
        - Copy `Vagrantfile.example` into `Vagrantfile`
        - Prompt you for your RedHat Developer Account credentials
            - If you do not have a developer account, [create one](https://www.redhat.com/en/developers).
        - Prompt you for the service account credentials for mounting `DVR`
        - Build your development VM
        
    - If you experience build errors, try re-provisioning (at most once):
    
    ```
    RH_USER=<Your RedHat Username> RH_PASS=<Your Redhat Password> \
    DVR_USER=<DVR Server Username> DVR_PASS=<DVR Server Password> vagrant provision
    ```
    
    - If you do not want to set the `RH_` environment variables and you don't mind having 
    your RedHat credentials stored in your `Vagrantfile`, you can add them on lines 4 and 5.

4. Run `vagrant ssh` to connect to your development environment.

5. Run `python manage.py runserver --host 0.0.0.0` to start the app.
You can access it on your browser at `localhost:8000`.
