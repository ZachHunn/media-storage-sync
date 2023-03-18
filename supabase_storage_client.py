from storage3 import create_client


url: str = ""
key: str = ""
headers = {'apiKey': key, 'Authorization': f"Bearer {key}"}
supabase_storage_client = create_client(url, headers, is_async=False)


def get_media_from_storage():
  media_list = []
  res = supabase_storage_client.from_('media').list()
  for media in res:
    media_name = media.get('name')
    media_type = media['metadata'].get('mimetype')
    media_url = supabase_storage_client.from_('media').get_public_url(media_name)
    
    media_list_dict = {"media_name": media_name, "media_type": media_type, "media_url": media_url}
    
    media_list.append(media_list_dict)

  return media_list


