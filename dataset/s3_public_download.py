import boto3

client = boto3.client('s3') #low-level functional API
resource = boto3.resource('s3') #high-level object-oriented API
finid = resource.Bucket('finid-public') #subsitute this for your s3 bucket name. 

folder = 'AN11102201'
s3_path = 'dataset/' + folder + '/'
#folder_year = FLAGS.FOLDER_YEAR + '/'

def get_all_s3_objects(s3, **base_kwargs):
    continuation_token = None
    while True:
        list_kwargs = dict(MaxKeys=1000, **base_kwargs)
        if continuation_token:
            list_kwargs['ContinuationToken'] = continuation_token
        response = s3.list_objects_v2(**list_kwargs)
        yield from response.get('Contents', [])
        if not response.get('IsTruncated'):  # At the end of the list?
            break
        continuation_token = response.get('NextContinuationToken')

#Getting a list of all images in the folder
obj_list = get_all_s3_objects(client, Bucket='finid', Prefix=s3_path)
images = list(finid.objects.filter(Prefix=s3_path)) #list of individual ObjectSummary's
# No of videos:
print('No. of images: ', len(images))

import itertools
obj_list_c = itertools.islice(obj_list, 1, len(images), 1)
#print(next(obj_list_c))

import os
import re
data_path = 's3_files/'
for content in obj_list_c:
    filename = content['Key'].split('/')
    print(filename[4])
    finid.download_file(content['Key'], os.path.join(data_path, filename[4]))

print('No. of images: ', len(images))

filename = sorted(os.listdir(data_path))
video_filename = filename[0].split('_')
print(len(filename), video_filename[0])
