# Artifactory CLI

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

python get-pip.py

git clone https://github.com/ssurivs/artifactory-cli.git

cd artifactory-cli/

pip install requests argparse validate_email validators

pip install --extra-index-url 'https://anonymous@artiola.jfrog.io/artifactory/api/pypi/pypi-local/simple' artifactory-cli

