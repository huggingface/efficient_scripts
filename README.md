# Efficient_scripts

Just a collection of script that are useful to speed up work.

## change_config.py

This script can be used to change the config of one or more config files.
In the beginning the script should be run without `--do_upload` to make sure the changed 
configs can be checked locally before uploading them to the respective git repos, *e.g.*:

```bash
./change_config.py --search_key patrickvonplaten/t5-tiny-ra --key max_length --value 10
```

Having checked that the configs look good locally, one can upload them
to the repective git repos. Adding the `--rf` arg force deletes previously cloned
model repos.

```bash
./change_config.py --search_key patrickvonplaten/t5-tiny-ra --key max_length --value 10 --rf --upload
```

## upload_a_rew_repo.py

This script can be used to create a new repo.
PS. That's my real password.

```bash
./upload_a_rew_repo.py --user patrickvonplaten --pw 12345678 --org google --model mt5-small
```

