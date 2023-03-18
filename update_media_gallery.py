"""
get a list of media already in the database
get a list of the photos in storage
compare the list to see the new photos
get the Media Name, Media Type, and Media Url 
Add new media object to the database
"""


from typing import List
from supabase import create_client as client, Client
from supabase_storage_client import get_media_from_storage

url: str = ""
key: str = ""
supabase: Client = client(url, key)

def get_medianame_from_database():
  media_from_database = []
  response = supabase.table('gallery').select('mediaName').execute()
  for media in response.data:
    media_name = media.get('mediaName')
    media_from_database.append(media_name)
  return media_from_database

def media_list_to_add(media_from_storage: List[dict], media_from_database: List[str]) -> List[str] | str:
  media_from_database_list_length: int = len(media_from_database)
  media_from_storage_list_length: int = len(media_from_storage) 
  
  match media_from_database_list_length:
    case _ if media_from_database_list_length == media_from_storage_list_length:
      return 'No new photos to upload from storage'
    case _ if media_from_database_list_length > media_from_storage_list_length:
      return 'There are more photos in the database than storage. Photos should come from storage'
    case _:
      media_to_add: List[str] = []
      for media in media_from_storage:
       if media.get('media_name') not in media_from_database:
         media_to_add.append(media)
      return media_to_add
 
def add_media_from_storage_to_database(media_list_to_add: List[dict]) -> None:
  for media in media_list_to_add:
    media_name = media.get('media_name')
    media_type = media.get('media_type')
    media_url = media.get('media_url')

    media_to_add = {
        'mediaName': media_name,
        'mediaType': media_type,
        'mediaUrl': media_url
    }
    print(media_to_add)
    supabase.table('gallery').insert(media_to_add).execute()

if __name__ == '__main__':
  database_media = get_medianame_from_database()
  storage_media = get_media_from_storage()
  media_to_add_from_storge = media_list_to_add(storage_media, database_media)
  
  if media_to_add_from_storge is not List[str]:
    print(media_to_add_from_storge)
  else:
    add_media_from_storage_to_database(media_to_add_from_storge)
  

