# ORTHANC

This is a Docker image configured to run [orthanc](http://book.orthanc-server.com/users/docker.html) with a simple postgres database.
```
git clone https://www.github.com/som/som-orthanc.git
cd som-orthanc
```
You probably want to change the configuration file username and password for the database, it's in [orthanc/orthanc.json](orthanc/orthanc.json). Then bring up the image.

```
docker-compose up -d
```

```
docker-compose build
```

ports 4242 and 8042 should connect to Orthanc, so you should be able to open [http://localhost](http://localhost) to see things. Note that we are using the web server (nginx) installed on the host, which doesn't have to be the case (we could use a docker image).

How do you see your images? Like this:

```
docker-compose ps
docker ps
```

You will probably want to shell into the image to look around. I usually do this (note that I got the name from the `ps` commands above:

```
docker-compose run --entrypoint=bash orthanc
```


# Uploading Dicom

Enter an interactive shell and run:

```
python /code/ImportDicom.py orthanc 8042 /data/incoming/
```



You can also add using `storescu` you can use the dcmtk Singularity / Docker images that I've generated. 
Both are provided, and can be run with [Singularity](http://singularity.lbl.gov) if in an environment without sudo, or 
with Docker on your local machine. 
Checkout out [pydicom](https://pydicom.github.io/containers-dcmtk) organization containers docs.

With `storescu` you can run:

```
storescu -aec SOMORTHANC localhost 4242 *.dcm
```


# Storage
The image uses an actual folder on the filesystem, which seems similar to MIRC-CTP's approach. 
In this instance, I found it here, along with the configuration file:

```
ls etc/orthanc
OrthancStorage orthanc.json
```

and you can tell this from the [docker-compose.yml](docker-compose.yml), but there are other database stuffs (eg postgres) here:

```
ls /var/lib/orthanc/db
ls /var/lib/postgresql
```
