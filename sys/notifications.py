import nvs, json

def addNotification(from_name, body_text):
  notification = readNotification()
  if len(notification['tree'])>0:
    ind=notification[-1]['id']+1
    notification['tree'].append({
                          'from': from_name,
                          'body': body_text,
                          'id': ind,
                      })
  if len(notification['tree'])>64:
    notification['tree']=notification[:-60]
  nvs.write(str('notification'), json.dumps(notification))

def removeNotification(id):
  notification = readNotification()
  if len(notification['tree'])>0:
    for i,d in enumerate(notification['tree']):
      if d['id']==id:
        notification['tree']['id'].pop(i)
        break
  nvs.write(str('notification'), json.dumps(notification))

def seenNotification(id):
  notification = readNotification()
  if len(notification['tree'])>0:
    for d in notification['tree']:
      if d['id']==id:
        notification['lastseen']=notification['tree']['id']
        nvs.write(str('notification'), json.dumps(notification))
        break

def readNotifications():
  notification = {}
  notification['lastseen'] = -1
  notification['tree'] = []
  try:
    notification = json.loads(str(nvs.read_str('notification')))
  except Exception as e:
    notification = {}
    notification['lastseen'] = -1
    notification['tree'] = []
  return notification