# Aweber API tools

## Needed tools

    - Python 2.6/2.7

## Requires

    - aweber_api
    - future

## Installation

```console
pip install --user -e git+https://github.com/foobar667/aweber_tools#egg=aweber_tools
```
or
```console
python setup.py install
```
or
```console
python setup.py sdist
pip install <path_to_sdist>
```

## Usage

There's an **Examples** directory in the source tree with the needed files.
Rename **config.cfg.example** to **config.cfg**, edit it to match your AWeber
keys and run
```python
python awtools.py
```

### Config format

```ini
[account]
consumer_key = spam
consumer_secret = ham
access_token = eggs
access_secret = cheese

[files]
backup_path = bacon
```

The **consumer_key** and **consumer_secret** values are required. Everything
else is optional.

### Access keys

**consumer_key** and **consumer_secret** are API application keys.
You can create one at https://labs.aweber.com.

More info at https://labs.aweber.com/getting_started/main.

**access_token** and **access_secret** are needed to grant the application
access to your AWeber account.
If these values are not set in the config file, the script will try to
authorize the application. Enter your AWeber account username and password
when prompted, and if all went well, the script will fetch access token and
access secret keys from AWeber and save them in the config file. Next time you
run the script, it'll use those values.

**Your username and password aren't stored anywhere.**

If the application can't authorize itself it will open AWeber's authorization
page in your default browser. Sign in there and copy the generated
**verification code** into the script's input prompt.

### API application permissions

If you're creating a new API application, set its application permissions to
**Request Subscriber Data**.