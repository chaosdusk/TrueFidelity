# Commands to reload server
```
sudo supervisorctl stop tf
sudo supervisorctl start tf
```

# To upload new images
```
flask shell
iu.create_batch("name", "description")
iu.upload_all("path to images folder", batch_id)
iu.upload_all_fake("path to noise folder", batch_id)
```