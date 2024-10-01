#!/bin/bash

aws s3 mb s3://ds2022-esd4uq
curl https://www.progarchives.com/progressive_rock_discography_covers/1492/cover_729151112017_r.jpg > pablohoney.jpg
aws s3 cp pablohoney.jpg s3://ds2022-esd4uq/
aws s3 ls s3://ds2022-esd4uq/
aws s3 presign --expires-in 604800  s3://ds2022-esd4uq/pablohoney.jpg

