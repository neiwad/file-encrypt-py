# Python File Encryptor

What is the purpose of this project?

Just to provide a simple file encryptor made with python.

## How to use?

### Encrypt file

```bash
python3 main your/file/location -e
```

Then enter a salt and a password

***Caution, this operation is irreversible if you loose or forget your salt / password.***

### Decrypt file

```bash
python3 main your/file/location -d
```

Then enter your salt and your password

## How to unit test functions?

```bash
python3 test.py
```

***Don't use this script if at at least one test fail. It could lead to some data corruption or permanent lock.***
