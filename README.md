# Correlation Analysis
This source code specifies an OpenShift image and job that runs correlation analysis for different combinations of the parser attributes used in rule development.

## Running locally
Clone this repository on your local machine and change working directory to local repository.

### Installing prerequisites
Install libraries listed in the requirements.txt.

To install all the dependencies at once, run the following command when inside the directory:
```
pip install -r requirements.txt
```
### Setting up credentials
Create a file named secret specifying the following attributes:

```
CEPH_S3_ACCESS_KEY=<value>
CEPH_S3_SECRET_KEY=<value>
CEPH_S3_ENDPOINT=<value>
CEPH_S3_BUCKET=<value>
PARAMS='{"PARSER_NAME": <value>, "COL_NAME": <value> "OUTFILE_NAME":<value>}'
CEPH_S3_PREFIX=<value>
```

Update the local path of secret file in run_local.sh bash script.

Run the bash script run_local.sh.

If everything worked well, you should obtain the graph's json in the CEPH folder specified through environment variables in the secret file. Also, the following output is displayed on the stdout:

```
Data collected from ParquetDataset
Graph Written to Ceph
```

## Deploying on OpenShift
Login OpenShift and set up project.

Optional: Modify app.yml as required.

Run the following command for creating image and build-config:

```
oc process -f app.yml | oc create -f -
```
Optional: Modify job.yml as required. By default, it takes secret environment variables from the application "insights-ds-analysis" but you can change it to your version of secrets by editing it in secret.ymnl and running:

```
oc process -f secret.yml | oc create -f -
```
Change the secretRef name to name of application in secret.yml.

Finally, run the following command:

```
oc process -f job.yml | oc create -f -
```
