# Efficient_scripts

Collection of scripts that should make your life easier when working with the HF model hub.

## change_config.py

This script can be used to change a parameter of multiple config files.
In the beginning the script should be run without `--do_upload` to make sure the changed 
configs can be checked locally before uploading them to the respective git repos, *e.g.*:

```bash
./change_config.py --search_key patrickvonplaten/t5-tiny-ra --key max_length --value 10
```

Having checked that the configs look as expected locally, one can upload them
to the repective git repos by adding `--do_upload`. Adding the `--rf` arg force deletes previously cloned
model repos.

```bash
./change_config.py --search_key patrickvonplaten/t5-tiny-ra --key max_length --value 10 --rf --upload
```

## upload_a_new_repo.py

This script can be used to quickly create a new repo.

```bash
./upload_a_new_repo.py --user patrickvonplaten --pw 12345678 --org google --model mt5-small
```
